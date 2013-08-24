from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from minimo.fattura.models import *
from minimo.cliente.models import *

        

class TemplateFatturaForm(forms.ModelForm):
    class Meta:
        model = TemplateFattura
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('descrizione'),
            Field('template'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super(TemplateFatturaForm, self).__init__(*args, **kwargs)
        
        
    def clean_template(self):
        filename = self.cleaned_data["template"]
        ext = os.path.splitext(filename.name)[1]
        ext = ext.lower()
        #print "clean_file value: %s" % ext
        if ext != ".odt" :
            raise forms.ValidationError("Il file deve avere estensione .odt!")
        return filename
    
    
class ImpostaForm(forms.ModelForm):
    
    
    class Meta:
        model = Imposta
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('aliquota'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
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
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super(RitenutaForm, self).__init__(*args, **kwargs)
        
        
class FatturaForm(forms.ModelForm):
    imposte = forms.ModelMultipleChoiceField(queryset=Imposta.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    ritenute = forms.ModelMultipleChoiceField(queryset=Ritenuta.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    stato = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    ragione_sociale = forms.CharField('Ragione sociale')
    class Meta:
        model = Fattura
        
        
    def __init__(self, *args, **kwargs):
        user_rid = kwargs.pop('user_rid')
        super(FatturaForm, self).__init__(*args, **kwargs)
        #self.fields['imposte'].queryset = Imposta.objects.filter(user_id=user_rid)
        self.fields['imposte'].queryset = Imposta.objects.filter()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    AppendedText('data', '<i class="icon-calendar"></i>'),
                    AppendedText('ragione_sociale', '<i class="icon-user"></i>'),
                    #Field('cliente'),
                    Field('stato'),
                    Field('template'),
                css_class="span6"),
                Div(
                    Field('imposte'),
                    Field('ritenute'),
                    Field('bollo'),
                    Field('valore_bollo'),
                css_class="span6"),
            css_class="row-fluid"),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
    


class FatturaInvioForm(forms.Form):
    mittente = forms.EmailField('Mittente')
    destinatario = forms.EmailField('Email destinatario')
    #cc_destinatario = forms.EmailField('Emaild destinatario per cc')
    oggetto = forms.CharField('Oggetto')
    messaggio = forms.CharField('Messaggio')
    
    def __init__(self,*args, **kwargs):
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_action = "/fatture/"
        self.helper.layout = Layout(
            AppendedText('mittente', '<i class="icon-user"></i>'),
            AppendedText('destinatario', '<i class="icon-user"></i>'),
            #AppendedText('cc_destinatario', '<i class="icon-user"></i>'),
            AppendedText('oggetto', '<i class="icon-notes"></i>'),
            AppendedText('messaggio', '<i class="icon-notes"></i>'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            ),
        )
        super(FatturaInvioForm, self).__init__(*args, **kwargs)
 
 
class PrestazioneForm(forms.ModelForm):
    
    
    class Meta:
        model = Prestazione
        exclude = ('fattura')
        
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('descrizione'),
            AppendedText('importo', '<i class="icon-money"></i>'),
            FormActions(
                Submit('save', 'Aggiungi', css_class="btn-primary")
            )
        )
        super(PrestazioneForm, self).__init__(*args, **kwargs)

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
                Button('save', 'Invia', css_class="btn-primary", onclick="aggiorna_statistiche();"),
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
                Submit('save', 'Invia', css_class="btn-primary")
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
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        
