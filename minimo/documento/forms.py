from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from minimo.documento.models import *
from minimo.cliente.models import *
    

class PagamentoaForm(forms.ModelForm):
    
    
    class Meta:
        model = Pagamento
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('giorni'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(PagamentoaForm, self).__init__(*args, **kwargs)      

class IncassaForm(forms.Form):
    
    importo = forms.FloatField()
       
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            AppendedText('importo', '<i class="icon-money"></i>'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(IncassaForm, self).__init__(*args, **kwargs)        
        
class DocumentoForm(forms.ModelForm):
    RITENUTA = lambda: [(m.nome, m.nome) for m in Ritenuta.objects.all()]
    #imposte = forms.ModelMultipleChoiceField(queryset=Imposta.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    descrizione_ritenuta = forms.ChoiceField(choices=RITENUTA(), required=False)
    stato = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    ragione_sociale = forms.CharField('Ragione sociale')
    
    class Meta:
        model = Documento
        
    
        
    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
  
        #self.fields['descrizione_ritenuta'].choices=RITENUTA()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('tipo'),
                    AppendedText('data', '<i class="icon-calendar"></i>'),
                    AppendedText('ragione_sociale', '<i class="icon-user"></i>'),
                    #Field('cliente'),
                    Field('stato'),
                    Field('template'),
                    Field('data_consegna'),
                    Field('sconto'),
                css_class="span6"),
                Div(
                    #Field('imposte'),
                    Field('descrizione_ritenuta'),
                    Field('bollo'),
                    Field('valore_bollo'),
                    Field('pagamento'),
                    Field('note'),
                css_class="span6"),
            css_class="row-fluid"),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
    


class FatturaInvioForm(forms.Form):
    mittente = forms.EmailField('Mittente')
    destinatario = forms.EmailField('Email destinatario')
    cc_destinatario = forms.EmailField('Emaild destinatario per cc', required=False)
    oggetto = forms.CharField('Oggetto')
    #TODO: visualizzare come textfield
    messaggio = forms.CharField('Messaggio')
    
    def __init__(self,*args, **kwargs):
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_action = "/fatture/"
        self.helper.layout = Layout(
            AppendedText('mittente', '<i class="icon-user"></i>'),
            AppendedText('destinatario', '<i class="icon-user"></i>'),
            AppendedText('cc_destinatario', '<i class="icon-user"></i>'),
            AppendedText('oggetto', '<i class="icon-notes"></i>'),
            AppendedText('messaggio', '<i class="icon-notes"></i>'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            ),
        )
        super(FatturaInvioForm, self).__init__(*args, **kwargs)
 
 
class RigaForm(forms.ModelForm):
    
    
    class Meta:
        model = Riga
        exclude = ('documento', 'imposta')
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('descrizione'),
            Field('quantita'),
            AppendedText('importo_unitario', '<i class="icon-money"></i>'),
            Field('descrizione_imposta'),
            FormActions(
                Submit('save', 'Aggiungi', css_class="btn-primary")
            )
        )
        super(RigaForm, self).__init__(*args, **kwargs)

class IntervalloForm(forms.Form):
    inizio = forms.DateField()
    fine = forms.DateField()
    
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "/bilancio/"
        self.helper.layout = Layout(
            AppendedText('inizio', '<i class="icon-calendar"></i>', css_class='span12'),
            AppendedText('fine', '<i class="icon-calendar"></i>', css_class='span12'),
            FormActions(
                Button('save', 'Salva', css_class="btn-primary", onclick="aggiorna_statistiche();"),
                Button('reset', 'Reset', onclick="reset_statistiche();"),
            ),
        )
        super(IntervalloForm, self).__init__(*args, **kwargs)

class LoginForm(AuthenticationForm):
    
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_method = 'post'
        #self.helper.form_action = "/login/"
        #self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('username', placeholder="username"),
            Field('password', placeholder="password"),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )

class PasswordForm(PasswordChangeForm):
    
    
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('old_password'),
            Field('new_password1'),
            Field('new_password2'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        
