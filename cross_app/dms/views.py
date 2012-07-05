# Create your views here.
import datetime
import os
from pydoc import Doc
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson
from cross_order.helper_functions import render_response
from dms.forms import DocumentUploadForm
from dms.helper import not_in_dms_group
from dms.models import Document, DocumentStatus, DocumentType
from settings import MEDIA_ROOT, LOGIN_URL

@login_required
@user_passes_test(not_in_dms_group, login_url=LOGIN_URL)
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
@user_passes_test(not_in_dms_group, login_url=LOGIN_URL)
def edit_row(request):
    try:
        d = Document.objects.get(pk=request.POST.get("row_id",0))
    except:
        return HttpResponse(simplejson.dumps("",default=dthandler),'application/json')
    d.ekol_doc_number = request.POST.get("value",0)
    d.save()
    return HttpResponse(simplejson.dumps(request.POST.get("value")).replace("\"",""),'application/json')

@login_required
@user_passes_test(not_in_dms_group, login_url=LOGIN_URL)
def list_documents(request):
    return render_response(request, 'dms/list_documents.html',
            {
                'docList':Document.objects.order_by('-upload_date'),
                'statusList':DocumentStatus.TYPE,
                'typeList':DocumentType.objects.all().order_by('order')
            })

@login_required
@user_passes_test(not_in_dms_group, login_url=LOGIN_URL)
def document_action(request):

    docList = request.POST.getlist('docChecked')
    if not len(docList) or "buttonSource" not in request.POST:
        return redirect('/dms/list_documents/')

    action = request.POST['buttonSource']
    if action == "update":
        for did in docList:
            s = request.POST.get("statusUpdate",None)
            if s is not None:
                d = Document.objects.get(pk=did)
                d.update_date = datetime.datetime.now()
                d.update_user = request.user
                d.status = int(s)
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
                'statusList':DocumentStatus.TYPE
            })