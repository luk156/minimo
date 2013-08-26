from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from minimo.tassa.models import *

class ImpostaForm(forms.ModelForm):
    
    
    class Meta:
        model = Imposta
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('aliquota'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(ImpostaForm, self).__init__(*args, **kwargs)  

class RitenutaForm(forms.ModelForm):
    
    
    class Meta:
        model = Ritenuta
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('aliquota'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(RitenutaForm, self).__init__(*args, **kwargs)

