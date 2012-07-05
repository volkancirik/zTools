from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from dms.models import Document

class DocumentUploadForm(ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'title','type')