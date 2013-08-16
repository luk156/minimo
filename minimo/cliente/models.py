# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg


import os

class Cliente(models.Model):
    user = models.ForeignKey(User, editable=False, related_name='cliente_user')
    ragione_sociale = models.CharField('Ragione sociale',max_length=70)
    via = models.CharField('Via',max_length=70)
    cap = models.CharField('CAP',max_length=6)
    citta = models.CharField('Citt?',max_length=70)
    provincia = models.CharField('Provincia',max_length=10)
    cod_fiscale = models.CharField('Codice Fiscale',max_length=50, blank=True, null=True)
    p_iva = models.CharField('Partita IVA',max_length=30, blank=True, null=True)
    telefono = models.CharField('Telefono', max_length=13, blank=True, null=True)
    mail = models.EmailField('E-mail',max_length=50, blank=True, null=True)
    
    def __unicode__(self):
        return '%s' % (self.ragione_sociale)

    def _get_indirizzo(self):
        return '%s, %s %s %s' %(self.via, self.cap, self.citta, self.provincia)
    
    indirizzo = property(_get_indirizzo)