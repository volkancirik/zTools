# Create your views here.
import datetime
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
#from dms.forms import DocumentUploadForm
from rts.helper import not_in_rts_warehouse_group, not_in_rts_customer_group
from rts.models import OrderItemBaseForReturns, ReturnedItemDetails,ReturnReason,ActionType,rts_status
from settings import MEDIA_ROOT, LOGIN_URL

@login_required
@user_passes_test(not_in_rts_warehouse_group, login_url=LOGIN_URL)

def search_returned_item(request):

    if request.method == 'POST':
        suborder_ = request.POST['suborder_nr']
        order_nr_ = request.POST['order_nr']
        try:
            oibfr_list = OrderItemBaseForReturns.objects.filter(suborder_number = suborder_,order_nr = order_nr_ )
            return render_response(request, 'rts/list_order_items.html',{
                'oibfr_list': oibfr_list,
                'actionList':ActionType.objects.all().order_by("order"),
                'reasonList':ReturnReason.objects.all().order_by("order"),
            })
        except:
            return render_response(request, 'rts/list_order_items.html',{
                'oibfr_list': None,
                'actionList':ActionType.objects.all().order_by("order"),
                'reasonList':ReturnReason.objects.all().order_by("order"),
            })
        
def list_all(request):

    try:
        suborderNumber = request.GET['suborder_nr']
        orderNumber = request.GET['order_nr']
        oibfr_list = OrderItemBaseForReturns.objects.filter(suborder_number = suborderNumber, order_nr = int(orderNumber)).exclude(returneditemdetails__status = rts_status.COMPLETED)
    except:
        oibfr_list = OrderItemBaseForReturns.objects.all().exclude(returneditemdetails__status  = rts_status.COMPLETED)
    return render_response(request, 'rts/list_order_items.html',{
        'oibfr_list': oibfr_list,
        'actionList':ActionType.objects.all().order_by("order"),
        'reasonList':ReturnReason.objects.all().order_by("order"),
    })

def update_returned_order(request):
    if request.method == 'POST':
        returnedOrder = OrderItemBaseForReturns.objects.get(id_sales_order_item = int(request.POST['returnedItemID']))
        returnReason = ReturnReason.objects.get(pk = int(request.POST['reasonList']))
        actionType = ActionType.objects.get(pk = int(request.POST['actionList']))
        comment = request.POST['comment']
        ReturnedItemDetails.objects.create(order_item = returnedOrder, return_reason = returnReason, action_type = actionType, comment = comment, create_user = request.user )
        return redirect('/rts/list_all/?suborder_nr='+returnedOrder.suborder_number+'&order_nr='+returnedOrder.order_nr)
