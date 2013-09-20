from django.db import models

class prodotto(models.Model):
    codice = models.CharField('Codice', max_length=30, blank=True, null=True, default=None)
    descrizione = models.CharField('Descrizione', max_length=70, blank=True, null=True, default=None)
    prezzo = models.FloatField('Prezzo unitario')

