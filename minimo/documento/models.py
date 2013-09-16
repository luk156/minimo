# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg
from minimo.cliente.models import *
from minimo.documento.utils import *
from minimo.template.models import *
from django.core.urlresolvers import reverse
from minimo.tassa.models import *
from datetime import datetime, timedelta


import os
import config



class Pagamento(models.Model):
    nome = models.CharField('Pagamento',max_length=30)
    giorni = models.IntegerField('Giorni', default=0)
    stato = models.BooleanField('Stato', default=True )
        
    
    def __unicode__(self):
        return self.nome
    
    def  giorni_scadenza(self):
        pass
    
    def scadenza(self, data):
        now = datetime.now().date()
        delta = data + timedelta(days=self.giorni)
        if now < delta :
            return False
        else:
            return True
    
    

TIPO_DOCUMENTO = (
    ('RA', 'Ritenuta acconto'),
    ('FA', 'Fattura'),
    ('PR', 'Preventivo'),
    ('OR', 'Ordine'),
    ('DT', 'Documento di trasporto'),
)

RITENUTA = ()


#TODO: implementare sconto

class Documento(models.Model):
    user = models.ForeignKey(User, editable=False)
    tipo = models.CharField('Tipo documento', max_length=5, choices=TIPO_DOCUMENTO)
    numero = models.IntegerField('Numero progressivo', editable=False, default=0, unique_for_year="data")
    data = models.DateField('Data di emissione')
    data_consegna = models.DateField('Data di consegna', null=True, blank=True)
    ragione_sociale = models.CharField('Ragione sociale',max_length=70,null=True, blank=True)
    via = models.CharField('Via',max_length=70, null=True, blank=True)
    cap = models.CharField('CAP',max_length=6, null=True, blank=True)
    citta = models.CharField('Citt?',max_length=70, null=True, blank=True)
    provincia = models.CharField('Provincia',max_length=10, null=True, blank=True)
    cod_fiscale = models.CharField('Codice Fiscale',max_length=50, blank=True, null=True)
    p_iva = models.CharField('Partita IVA',max_length=30, blank=True, null=True)
    stato = models.BooleanField('Stato pagamento')
    template = models.ForeignKey(TemplateDocumento, related_name='documento_template', null = True, on_delete = models.SET_NULL)
    descrizione_ritenuta = models.CharField('Descrizione ritenuta', max_length=70, null=True, blank=True, choices=RITENUTA)
    ritenuta = models.IntegerField('Ritenuta', blank=True, null=True, default=None)
    bollo = models.CharField('ID Bollo',max_length=30, blank=True, null=True)
    valore_bollo = models.FloatField('Valore marca da bollo', blank=True, null=True)
    pagamento = models.ForeignKey(Pagamento, verbose_name="condizioni pagamento", blank=True, null=True)
    riferimento = models.ForeignKey('Documento', verbose_name="Documento collegato", blank=True, null=True)
    note = models.TextField('Note', max_length=1024, null=True, blank=True)
    sconto = models.IntegerField('Sconto', blank=True, null=True, default=None)
    importo_residuo = models.FloatField('Importo residuo da incassare', blank=True, null=True)
    
    
    def __unicode__(self):
        return '%s-%s' % (self.progressivo(),self.data.year)
    
    def _get_tipo_documento(self):
        if self.tipo == 'RA':
            return "Ritenuta d'acconto"
        if self.tipo == 'FA':
            return "Fattura"
        if self.tipo == 'PR':
            return "Preventivo"
        if self.tipo == 'OR':
            return "Ordine"
    
    tipo_documento = property(_get_tipo_documento)
    
    def _get_righe(self):
        righe = Riga.objects.filter(documento=self)
        return righe
    
    righe = property(_get_righe)
    
    class Meta:
        ordering = ['data']
        
            
    def imponibile(self):
        tot=0
        #calcolo con iva
        if not self.ritenuta:
            for p in self.righe:
                tot += p.totale_netto
            return round(tot,2)
        #calcolo con ritenuta
        if self.ritenuta:
            tot = self.totale 
            if self.valore_bollo:
                tot -= self.valore_bollo
            tot = tot + self.tot_ritenute
            return round(tot,2)
    
    
    def _imposta_totale(self):
        t=0
        for p in self.righe:
            t += p.totale_imposta
        return round(t,2)
    
    imposta_totale = property(_imposta_totale)

    def _tot_ritenute(self):
        if self.ritenuta:
            tot = self.totale
            if self.valore_bollo:
                tot -= self.valore_bollo
            perc = (100-self.ritenuta)/100.0
            lordo = tot / perc
            return round(lordo - tot , 2)
        else:
            return 0
        
    
    tot_ritenute = property(_tot_ritenute)
    
    def _totale(self):
        tot = 0
        #caloclo con iva
        if not self.ritenuta:
            for p in self.righe:
                tot += p.totale_lordo
            if self.valore_bollo:
                tot += self.valore_bollo
            return round(tot,2)
        #calcolo con ritenuta
        if self.ritenuta:
            for p in self.righe:
                tot += p.totale_netto
            if self.valore_bollo:
                tot += self.valore_bollo
            return round(tot,2)
    
    totale = property(_totale)
      
    def progressivo(self):
        return self.numero
    
    def _get_cliente(self):
        try:
            cliente = Cliente.objects.get(ragione_sociale=self.ragione_sociale)
        except Exception:
            cliente = None
        return cliente
    
    cliente = property(_get_cliente)
    
    def _stato_documento(self):
        if self.stato:
            if self.tipo == 'RA' or self.tipo == 'FA':
                return "Pagato"
            else:
                return "Accettato"
        else:
            if self.tipo == 'RA' or self.tipo == 'FA':
                return "Da pagare"
            else:
                return "In attesa accettazione"

    
    stato_documento = property(_stato_documento)
    
    def _scaduto(self):
        if not self.stato and self.pagamento:
            return self.pagamento.scadenza(self.data)
        else:
            return False
    
    scaduto = property(_scaduto)
    
    def save(self, *args, **kwargs):          
        if self.numero == 0:
            d_anno = Documento.objects.filter(data__year=self.data.year, tipo=self.tipo).aggregate(Max('numero'))
            if not d_anno['numero__max']:
                d_anno['numero__max'] = 0
            self.numero = d_anno['numero__max'] + 1   
        super(Documento, self).save(*args, **kwargs)
        


         

class Riga(models.Model):
    codice = models.CharField('Codice', max_length=70, blank=True, null=True, default=None)
    descrizione = models.TextField('Descrizione')
    quantita = models.FloatField('Quantità')
    importo_unitario = models.FloatField('Prezzo unitario', default=1)
    descrizione_imposta = models.CharField('Descrizione Imposta', max_length=70, blank=True, null=True, default=None)
    imposta = models.IntegerField('Imposta', blank=True, null=True, default=None)
    documento = models.ForeignKey(Documento)
    
    def _totale_netto(self):
        return self.quantita * self.importo_unitario
    
    #importo = property(_totale_netto)
    totale_netto = property(_totale_netto)
    
    def _totale_lordo(self):
        return self.totale_netto + self.totale_imposta
    
    totale_lordo = property(_totale_lordo)
    
    def _totale_imposta(self):
        if self.imposta:
            return round(self.totale_netto*(self.imposta/100.0), 2)
        else:
            return 0
    totale_imposta = property(_totale_imposta)
    
    def __unicode__(self):
        return '%s(%s)' % (self.descrizione,self.totale_netto)
    
    def save(self, *args, **kwargs):
        print  self.descrizione_imposta

        try:
            self.imposta = Imposta.objects.get(nome=self.descrizione_imposta).aliquota
        except Exception:
            print 'ko'
        
        super(Riga, self).save(*args, **kwargs)


