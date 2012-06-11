# Create your views here.
import datetime
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
from dms.forms import DocumentUploadForm
from dms.models import Document
from settings import MEDIA_ROOT

@login_required
def upload_document(request):

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST,request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.file = request.FILES['file']
            doc.upload_user = request.user
            doc.upload_date = datetime.datetime.now()
            doc.save()
            return redirect('/dms/list_documents/')
        else:
            return render_response(request, 'dms/upload_document.html',{'form':form})
    else:
        return render_response(request, 'dms/upload_document.html',{'form':DocumentUploadForm()})


@login_required
def list_documents(request):
    return render_response(request, 'dms/list_documents.html',
            {
                'docList':Document.objects.order_by('-upload_date'),
            })

@login_required
def document_action(request):

    docList = request.POST.getlist('docChecked')
    if not len(docList) or "buttonSource" not in request.POST:
        return redirect('/dms/list_documents/')

    action = request.POST['buttonSource']
    if action == "update":
        for did in docList:
            d = Document.objects.get(pk=did)
            d.update_date = datetime.datetime.now()
            d.update_user = request.user
            d.save()
    elif action == "delete":
        for did in docList:
            d = Document.objects.get(pk=did)
            #fname = d.file.name
            d.delete()
            #os.unlink(MEDIA_ROOT+fname)
            
    return render_response(request, 'dms/list_documents.html',
            {
                'docList':Document.objects.order_by('-upload_date'),
            })