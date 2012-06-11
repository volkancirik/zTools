from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from dms.models import Document

class DocumentUploadForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('comment','upload_user', 'upload_date','update_user', 'update_date','downloadCount')