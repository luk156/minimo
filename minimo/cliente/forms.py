from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from minimo.cliente.models import *


class ClienteForm(forms.ModelForm):
    #indirizzo=forms.CharField(widget = forms.Textarea(),)
    class Meta:
        model = Cliente
        
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
            Div( Field('ragione_sociale'),
                Field('via'),
                Field('cap'),
                Field('citta'),
                Field('provincia'),
                css_class="span6"),
            Div( Field('cod_fiscale'),
                Field('p_iva'),
                AppendedText('telefono', '<i class="icon-phone"></i>'),
                AppendedText('mail', '<i class="icon-envelope"></i>'),
                css_class="span6"), css_class="row-fluid"),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super( ClienteForm, self).__init__(*args, **kwargs)