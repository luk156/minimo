# -*- coding: utf-8 -*-

from django.db import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg


import os
# Create your models here.

class Cliente(models.Model):
    user = models.ForeignKey(User, editable=False, related_name='cliente_user')
    ragione_sociale = models.CharField('Ragione sociale',max_length=70)
    via = models.CharField('Via',max_length=70)
    cap = models.CharField('CAP',max_length=6)
    citta = models.CharField('Città',max_length=70)
    provincia = models.CharField('Provincia',max_length=10)
    cod_fiscale = models.CharField('Codice Fiscale',max_length=50, blank=True, null=True)
    p_iva = models.CharField('Partita IVA',max_length=30, blank=True, null=True)
    telefono = models.CharField('Telefono', max_length=13, blank=True, null=True)
    mail = models.EmailField('E-mail',max_length=50, blank=True, null=True)
    
    def __unicode__(self):
        return '%s' % (self.ragione_sociale)

    def _get_indirizzo(self):
        return '%s, %s %s %s' %(self.via, self.cap, self.citta, self.provincia)
    
    indirizzo = property(_get_indirizzo)

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

def content_file_name(instance, filename):
    return '/'.join(['content', "template-"+str(instance.nome)+".odt"])

class TemplateFattura(models.Model):
    user=models.ForeignKey(User, editable=False, related_name='template_user')
    nome = models.CharField('Nome',max_length=70, unique=True)
    descrizione = models.CharField('Descrizione',max_length=70, blank=True, null=True)
    template = models.FileField(upload_to=content_file_name)
    def __unicode__(self):
        return '%s' % (self.nome)
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TemplateFattura.objects.get(id=self.id)
            if this.template != self.template:
                this.template.delete(save=False)
        except:
            pass # when new photo then we do nothing, normal case          
        super(TemplateFattura, self).save(*args, **kwargs)

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

class Imposta(models.Model):
    user=models.ForeignKey(User, editable=False, related_name='imposta_user')
    nome=models.CharField('Nome Imposta',max_length=30)
    aliquota=models.FloatField('Aliquota')
    def calcola(self,imponibile):
        return round(imponibile*self.aliquota/100.0,2)
    def __unicode__(self):
        return '%s (%s %%)' % (self.nome, str(self.aliquota))

class Ritenuta(models.Model):
    user=models.ForeignKey(User, editable=False, related_name='ritenuta_user')
    nome=models.CharField('Nome Ritenuta',max_length=30)
    aliquota=models.FloatField('Aliquota')
    def calcola(self,imponibile):
        return round(imponibile*self.aliquota/100.0,2)
    def __unicode__(self):
        return '%s (%s %%)' % (self.nome, str(self.aliquota))   


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

class Fattura(models.Model):
    user=models.ForeignKey(User, editable=False, related_name='fattura_user')
    numero = models.IntegerField('Numero progressivo', editable=False, default=0, unique_for_year="data")
    data=models.DateField('Data di emissione')
    cliente=models.ForeignKey(Cliente, related_name='fattura_cliente', null = True, on_delete = models.SET_NULL)    
    stato=models.BooleanField('Stato pagamento')
    template=models.ForeignKey(TemplateFattura, related_name='fattura_template', null = True, on_delete = models.SET_NULL)
    imposte=models.ManyToManyField(Imposta,  blank=True, null = True)
    ritenute=models.ManyToManyField(Ritenuta,  blank=True, null = True)
    bollo=models.CharField('ID Bollo',max_length=30, blank=True, null=True)
    valore_bollo=models.FloatField('Valore marca da bollo', blank=True, null=True)
    def __unicode__(self):
        
        
        return '%s-%s' % (self.progressivo(),self.data.year)
    class Meta:
        ordering = ['data']
        
        
    def imponibile(self):
        i=0
        for p in self.prestazione_fattura.all():
            i+=p.importo
        return round(i,2)
    

    def tot_imposte(self):
        t=0
        for i in self.imposte.all():
            t+=i.calcola(self.imponibile())
        return round(t,2)
    

    def tot_ritenute(self):
        r=0
        for i in self.ritenute.all():
            r+=i.calcola(self.imponibile())
        return round(r,2)
    

    def totale(self):
        tot = self.imponibile()+self.tot_imposte()-self.tot_ritenute()
        if self.valore_bollo:
            tot+=self.valore_bollo
        return round(tot,2)
    

    def progressivo(self):
        return self.numero
    
    
    def save(self, *args, **kwargs):
        if self.numero == 0:
            fatture_anno=Fattura.objects.filter(data__year=self.data.year).aggregate(Max('numero'))
            if not fatture_anno:
		fatture_anno = 0
            self.numero = fatture_anno['numero__max'] + 1
        super(Fattura, self).save(*args, **kwargs)


class FatturaForm(forms.ModelForm):
    class Meta:
        model = Fattura
    def __init__(self, *args, **kwargs):
        user_rid = kwargs.pop('user_rid')
        super(FatturaForm, self).__init__(*args, **kwargs)
        self.fields['imposte'].queryset = Imposta.objects.filter(user_id=user_rid)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    AppendedText('data', '<i class="icon-calendar"></i>'),
                    Field('cliente'),
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
        

class Prestazione(models.Model):
    descrizione=models.TextField('Descrizione')
    importo=models.FloatField('Importo')
    fattura=models.ForeignKey(Fattura, related_name='prestazione_fattura')  
    def __unicode__(self):
        return '%s(%s)' % (self.descrizione,self.importo)


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
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super(PrestazioneForm, self).__init__(*args, **kwargs)

class IntervalloForm(forms.Form):
    inizio=forms.DateField()
    fine=forms.DateField()
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
        

