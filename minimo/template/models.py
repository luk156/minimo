# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg
from datetime import datetime, timedelta

import os

def content_file_name(instance, filename):
    return '/'.join(['content', "template-"+str(instance.nome)+".odt"])


class TemplateDocumento(models.Model):
    user = models.ForeignKey(User, editable=False)
    nome = models.CharField('Nome',max_length=70, unique=True)
    descrizione = models.CharField('Descrizione',max_length=70, blank=True, null=True)
    template = models.FileField(upload_to=content_file_name)
    
    
    def __unicode__(self):
        return '%s' % (self.nome)
    
    
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TemplateDocumento.objects.get(id=self.id)
            if this.template != self.template:
                this.template.delete(save=False)
        except:
            pass # when new photo then we do nothing, normal case          
        super(TemplateDocumento, self).save(*args, **kwargs)
