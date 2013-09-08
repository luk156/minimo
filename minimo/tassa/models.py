# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Imposta(models.Model):
    user = models.ForeignKey(User, editable=False)
    nome = models.CharField('Nome Imposta',max_length=30)
    aliquota = models.IntegerField('Aliquota')
    
    class Meta:
        verbose_name = _('imposta')
        verbose_name_plural=_('Imposte')
        ordering=['nome']
    
    def calcola(self,totale_netto):
        return round(totale_netto*self.aliquota/100.0,2)
    
    
    def __unicode__(self):
        return '%s (%s %%)' % (self.nome, str(self.aliquota))

class Ritenuta(models.Model):
    user = models.ForeignKey(User, editable=False)
    nome = models.CharField('Nome Ritenuta',max_length=30)
    aliquota = models.FloatField('Aliquota')
    
    class Meta:
        verbose_name = _('Ritenuta')
        verbose_name_plural=_('ritenute')
        ordering=['nome']
        
        
    def calcola(self,totale_netto):
        perc = (100-self.aliquota)/100.0
        lordo = totale_netto / perc
        return round(lordo - totale_netto , 2)
    
    def __unicode__(self):
        return '%s (%s %%)' % (self.nome, str(self.aliquota)) 