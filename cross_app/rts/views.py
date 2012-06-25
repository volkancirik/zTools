# Create your views here.
import datetime
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
#from dms.forms import DocumentUploadForm
from rts.helper import not_in_rts_group
from rts.models import OrderItemBaseForReturns, ReturnedItemDetails,ReturnReason,ActionType
from settings import MEDIA_ROOT, LOGIN_URL

@login_required
#@user_passes_test(not_in_rts_group, login_url=LOGIN_URL)
def search_page(request):
    return render_response(request, 'rts/search_page.html',{})

def search_returned_item(request):

    if request.method == 'POST':
        suborder_ = request.POST['suborder_nr']
        order_nr_ = request.POST['order_nr']
        try:
            oibfr_list = OrderItemBaseForReturns.objects.filter(suborder_number = suborder_,order_nr = order_nr_ )
            return render_response(request, 'rts/list_order_items.html',{'oibfr_list': oibfr_list})
        except:
            return render_response(request, 'rts/list_order_items.html',{'oibfr_list': None})
def list_all(request):
    oibfr_list = OrderItemBaseForReturns.objects.all()
    return render_response(request, 'rts/list_order_items.html',{'oibfr_list': oibfr_list})