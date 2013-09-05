from minimo.cliente.models import *
from minimo.documento.models import *

def copia_dati_fiscali(documento, cliente):
    documento.ragione_sociale = cliente.ragione_sociale
    documento.via = cliente.via
    documento.cap = cliente.cap
    documento.citta = cliente.citta
    documento.provincia = cliente.provincia
    documento.p_iva = cliente.p_iva
    documento.cod_fiscale = cliente.cod_fiscale
    documento.save()  
