from minimo.cliente.models import *
from minimo.fattura.models import *

def copia_dati_fiscali(fattura, cliente):
    fattura.ragione_sociale = cliente.ragione_sociale
    fattura.via = cliente.via
    fattura.cap = cliente.cap
    fattura.citta = cliente.citta
    fattura.provincia = cliente.provincia
    fattura.p_iva = cliente.p_iva
    fattura.cod_fiscale = cliente.cod_fiscale
    fattura.save()  
