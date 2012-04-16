from django.db import models
from django.forms.models import ModelForm

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield



class ProjectForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = Project