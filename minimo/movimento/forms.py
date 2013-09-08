from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *


from minimo.movimento.models import *
    

class RegistraDocumentoForm(forms.ModelForm):
    
    
    class Meta:
        model = FattureFornitore
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('tipo'),
            Field('data'),
            Field('scadenza_pagamento'),
            Field('numero'),
            Field('descrizione'),
            Field('importo'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(RegistraDocumentoForm, self).__init__(*args, **kwargs)