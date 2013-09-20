from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *


from minimo.movimento.models import *
    

class RegistraDocumentoForm(forms.ModelForm):
    
    
    class Meta:
        model = FattureFornitore
        
    def __init__(self, *args, **kwargs):
        print '0'
        super(RegistraDocumentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('tipo'),
            Field('data_documento'),
            Field('scadenza_pagamento'),
            Field('numero'),
            Field('descrizione'),
            #Field('allegato'),
            Field('importo'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        
    
    def clean_allegato(self):
        print 'o'
        filename = self.cleaned_data["allegato"]
        return filename
    
class MovimentoForm(forms.ModelForm):
    
    class Meta:
        model = Movimento
        exclude = ('documento', 'conto')
      
    def __init__(self, *args, **kwargs):  
        super(MovimentoForm, self).__init__(*args, **kwargs)
      
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('tipo'),
                    AppendedText('data_movimento', '<i class="icon-calendar"></i>'),
                    Field('descrizione'),
                    Field('importo'),
                css_class="span6"),
                
            css_class="row-fluid"),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        
    
    
    
    