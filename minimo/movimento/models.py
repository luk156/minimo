# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg
from minimo.cliente.models import *
from minimo.documento.utils import *
from minimo.template.models import *
from django.core.urlresolvers import reverse
from minimo.tassa.models import *
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import os




class Conto(models.Model):
    nome = models.CharField('Nome conto', max_length=70)
    iban = models.CharField('IBAN', max_length=70, null=True, blank=True)
    istituto = models.CharField('Istituto bancario',max_length=70, null=True, blank=True)
    intestazione = models.CharField('Intestato',max_length=70, null=True, blank=True)
    saldo = importo = models.FloatField('Saldo', default=0)
    data_ultimo_aggiornamento = models.DateField('Data ultimo aggiornamento', auto_now=True)
    
    class Meta:
        verbose_name = 'Conto'
        verbose_name_plural='Conti'
        ordering=['nome']
        
TIPO = (
        ('E', 'Entrata'),
        ('U', 'Uscita'),
    )

class Movimento(models.Model):
    user = models.ForeignKey(User, editable=False)
    conto = models.ForeignKey('Conto', null=True, blank=True)
    tipo = models.CharField('Tipo movimento', max_length=70, choices=TIPO)
    data_movimento = models.DateField('Data movimnto', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField( null=True, blank=True)
    documento = generic.GenericForeignKey('content_type', 'object_id')
    descrizione = models.TextField('Descrizione', max_length=1024, null=True, blank=True)
    importo = models.FloatField('Importo')

    class Meta:
        verbose_name = 'Movimento'
        verbose_name_plural='Movimenti'
        ordering=['data_movimento']

    def __unicode__(self):
        return "%s - %s %s" %(self.tipo, self.descrizione, self.importo)
    
    def get_documento(self):
        return self.documento
    
    def _get_importo(self, ):
        if self.tipo == 'E':
            return self.importo
        else:
            return -self.importo
        
    valore_importo = property(_get_importo)
    
    def save(self, *args, **kwargs):
        aggiorna_saldo(nome=None, importo=self.importo, operazione=self.tipo)
        super(Movimento, self).save(*args, **kwargs)
        

TIPO_FATTURA = (
    ('F', 'Fornitore'),
    ('S', 'Servizi'),
)



class FattureFornitore(models.Model):

    user = models.ForeignKey(User, editable=False)
    tipo = models.CharField('Tipo fattura', max_length=70, choices=TIPO_FATTURA)
    data_documento = models.DateField('Data Emissione documento', null=True, blank=True)
    numero = models.CharField('Numero documento', max_length=70)
    scadenza_pagamento = models.DateField('Data scadenza documento', null=True, blank=True)
    descrizione = models.TextField('Descrizione', max_length=1024, null=True, blank=True)
    importo = models.FloatField('Importo')
    stato = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Fatture Fornitore'
        verbose_name_plural='Fatture Fornitore'
        ordering=['data_documento']

    def __unicode__(self):
        return "%s %s" %(self.tipo,  self.importo)
    

class ContoOption(admin.ModelAdmin):
    pass


def aggiorna_saldo(nome=None, importo=0, operazione=''):
    if nome == None:
        conto, created = Conto.objects.get_or_create(nome='default')
        if created:
            conto.numero='000000'
            conto.importo = 0
            conto.save()
    else:
        conto = Conto.objects.get(nome=nome)
    if operazione == 'E':
        conto.saldo += importo
    if operazione == 'U':
        conto.saldo -= importo
    conto.save()


def ripristina_saldo(nome=None, importo=0, operazione=''):
    if nome == None:
        conto, created = Conto.objects.get_or_create(nome='default')
        if created:
            conto.numero='000000'
            conto.importo = 0
            conto.save()
    else:
        conto = Conto.objects.get(nome=nome)
    if operazione == 'U':
        conto.saldo += importo
    if operazione == 'E':
        conto.saldo -= importo
    conto.save()


def get_conto(nome=None):
    if nome == None:
        conto, created = Conto.objects.get_or_create(nome='default')
        if created:
            conto.numero='000000'
            conto.importo = 0
            conto.save()
    else:
        conto = Conto.objects.get(nome=nome)
    return conto



admin.site.register(Conto, ContoOption)
