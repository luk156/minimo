import logging
import sys, os, socket, re
from django.core.management.base import NoArgsCommand
from django.db.models import Avg, Sum

from minimo.documento.models import *

from datetime import datetime, timedelta


class Command(NoArgsCommand):
    help = "genera le medie."
    
    def handle_noargs(documento, **options):
        fatture = Fattura.objects.all()
        print len(fatture)
        conv = 0
        for documento in fatture:
            #codice per recuperare dati da vecchia versione del db
            documento.ragione_sociale = documento.cliente.ragione_sociale
            documento.via = documento.cliente.via
            documento.cap = documento.cliente.cap
            documento.citta = documento.cliente.citta
            documento.provincia = documento.cliente.provincia
            documento.p_iva = documento.cliente.p_iva
            documento.cod_fiscale = documento.cliente.cod_fiscale
            documento.save()
            print documento.ragione_sociale
            conv += 1
        print "convertite %s fatture" %conv
                