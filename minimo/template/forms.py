from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *


from minimo.template.models import *

        

class TemplateDocumentoForm(forms.ModelForm):
    class Meta:
        model = TemplateDocumento
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('descrizione'),
            Field('template'),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )
        super(TemplateDocumentoForm, self).__init__(*args, **kwargs)
        
        
    def clean_template(self):
        filename = self.cleaned_data["template"]
        ext = os.path.splitext(filename.name)[1]
        ext = ext.lower()
        #print "clean_file value: %s" % ext
        if ext != ".odt" :
            raise forms.ValidationError("Il file deve avere estensione .odt!")
        return filename
    
    