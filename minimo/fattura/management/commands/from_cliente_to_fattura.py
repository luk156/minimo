import logging
import sys, os, socket, re
from django.core.management.base import NoArgsCommand
from django.db.models import Avg, Sum

from minimo.fattura.models import *

from datetime import datetime, timedelta


class Command(NoArgsCommand):
    help = "genera le medie."
    
    def handle_noargs(fattura, **options):
        fatture = Fattura.objects.all()
        print len(fatture)
        conv = 0
        for fattura in fatture:
            #codice per recuperare dati da vecchia versione del db
            fattura.ragione_sociale = fattura.cliente.ragione_sociale
            fattura.via = fattura.cliente.via
            fattura.cap = fattura.cliente.cap
            fattura.citta = fattura.cliente.citta
            fattura.provincia = fattura.cliente.provincia
            fattura.p_iva = fattura.cliente.p_iva
            fattura.cod_fiscale = fattura.cliente.cod_fiscale
            fattura.save()
            print fattura.ragione_sociale
            conv += 1
        print "convertite %s fatture" %conv
                