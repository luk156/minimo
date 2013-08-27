# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg
from minimo.cliente.models import *
from minimo.fattura.utils import *
from minimo.template.models import *
from minimo.template.models import *
from datetime import datetime, timedelta

import os
import config


TIPO_PREVENTIVO = (
    ('OF', 'Offerta cliente'),
    ('OR', 'Ordine cliente'),
)

TIPO_DOCUMENTO = (
    ('FA', 'Fattura'),
    ('RA', 'Ritenuta'),
)

STATO_DOCUMENTO = (
    ('BZ', 'Bozza'),
    ('IN', 'Inviata'),
    ('IC', 'In corso'),
    ('CF', 'Confermato'),
    ('FA', 'Fatturato'),
    ('AN', 'Annullato'),
)

class Preventivo(models.Model):
    user = models.ForeignKey(User, editable=False, related_name='fattura_user')
    tipo_preventivo = models.CharField('Tipo preventivo', max_length=5, choices=TIPO_DOCUMENTO)
    tipo_documento = models.CharField('Tipo documento', max_length=5, choices=TIPO_PREVENTIVO)
    numero = models.IntegerField('Numero progressivo', editable=False, default=0, unique_for_year="data")
    data = models.DateField('Data di emissione')
    data_consegna = models.DateField('Data di consegna prevista',null=True, blank=True)
    ragione_sociale = models.CharField('Ragione sociale',max_length=70,null=True, blank=True)
    via = models.CharField('Via',max_length=70, null=True, blank=True)
    cap = models.CharField('CAP',max_length=6, null=True, blank=True)
    citta = models.CharField('Citt?',max_length=70, null=True, blank=True)
    provincia = models.CharField('Provincia',max_length=10, null=True, blank=True)
    cod_fiscale = models.CharField('Codice Fiscale',max_length=50, blank=True, null=True)
    p_iva = models.CharField('Partita IVA',max_length=30, blank=True, null=True)
    stato = models.models.CharField('Stato documento', max_length=5, choices=STATO_DOCUMENTO)
    template = models.ForeignKey(TemplateDocumento, null = True, on_delete = models.SET_NULL)
    descrizione_ritenuta = models.CharField('Descrizione ritenuta', null=True, blank=True, max_length=70)
    ritenuta = models.IntegerField('Ritenuta', blank=True, null=True, default=None)
    bollo = models.CharField('ID Bollo',max_length=30, blank=True, null=True)
    valore_bollo = models.FloatField('Valore marca da bollo', blank=True, null=True)
    pagamento = models.ForeignKey('Pagamento previsto', verbose_name="condizioni pagamento", blank=True, null=True)
    
    
    def __unicode__(self):
        return '%s-%s' % (self.progressivo(),self.data.year)
    
    
    class Meta:
        ordering = ['data']
        
        
    def imponibile(self):
        tot=0
        if self.tipo == 'FA':
            for p in self.prestazione_fattura.all():
                tot += p.totale_netto
                print tot
            if self.valore_bollo:
                tot += self.valore_bollo
            return round(tot,2)
        if self.tipo == 'RA':            
            tot = self.totale() + self.tot_ritenute
            if self.valore_bollo:
                tot += self.valore_bollo
            return round(tot,2)
    
    
    def iva_totale(self):
        t=0
        for p in self.prestazione_fattura.all():
            t += p.totale_iva
        return round(t,2)
    

    def _tot_ritenute(self):
        perc = (100-self.ritenuta)/100.0
        lordo = totale_netto / perc
        return round(lordo - totale_netto , 2)
    
    tot_ritenute = property(_tot_ritenute)
    
    def totale(self):
        tot = 0
        if self.tipo =='FA':
            for p in self.prestazione_fattura.all():
                tot += p.totale_lordo
            if self.valore_bollo:
                tot += self.valore_bollo
            return round(tot,2)
        if self.tipo == 'RA':
            for p in self.prestazione_fattura.all():
                tot += p.totale_netto
            
            return round(tot,2)
        
    def progressivo(self):
        return self.numero
    
    def _get_cliente(self):
        try:
            cliente = Cliente.objects.get(ragione_sociale=self.ragione_sociale)
        except Exception:
            cliente = None
        return cliente
    
    cliente = property(_get_cliente)
    

    
    def save(self, *args, **kwargs):
        try:
            self.iva = Ritenuta.objects.get(nome=self.descrizione_ritenuta).aliquota
        except Exception:
            self.iva = 0
        if self.numero == 0:
            p_anno = Preventivo.objects.filter(data__year=self.data.year).aggregate(Max('numero'))
            if not p_anno['numero__max']:
                p_anno['numero__max'] = 0
            self.numero = p_anno['numero__max'] + 1   
        super(Preventivo, self).save(*args, **kwargs)
        


         

class Prestazione(models.Model):
    descrizione = models.TextField('Descrizione')
    quantita = models.FloatField('Quantità')
    importo_unitario = models.FloatField('Prezzo unitario', default=1)
    descrizione_iva = models.CharField('Iva', max_length=70, blank=True, null=True, default=None)
    iva = models.IntegerField('IVA', blank=True, null=True, default=None)
    #importo = models.FloatField('Importo')
    preventivo = models.ForeignKey(Preventivo)
    
    def _totale_netto(self):
        return self.quantita * self.importo_unitario
    
    importo = property(_totale_netto)
    totale_netto = property(_totale_netto)
    
    def _totale_lordo(self):
        return self.totale_netto + self.totale_iva
    
    totale_lordo = property(_totale_lordo)
    
    def _totale_iva(self):
        print 'iva:', (self.iva/100), 'netto:', self.totale_netto
        return round(self.totale_netto*(self.iva/100.0), 2)
    totale_iva = property(_totale_iva)
    
    def __unicode__(self):
        return '%s(%s)' % (self.descrizione,self.importo)
    
    def save(self, *args, **kwargs):
        try:
            self.iva = Imposta.objects.get(nome=self.descrizione_iva).aliquota
        except Exception:
            self.iva = 0
        
        super(Prestazione, self).save(*args, **kwargs)


