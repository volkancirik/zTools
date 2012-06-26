# Create your views here.

from datetime import  datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
#from dms.forms import DocumentUploadForm
from rts.helper import not_in_rts_warehouse_group, not_in_rts_customer_group
from rts.models import OrderItemBaseForReturns, ReturnedItemDetails,ReturnReason,ActionType,rts_status, RefundedItemDetails
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
        oibfr_list = OrderItemBaseForReturns.objects.all().exclude(returneditemdetails__status  = rts_status.REFUNDED)
    return render_response(request, 'rts/list_order_items.html',{
        'oibfr_list': oibfr_list,
        'actionList':ActionType.objects.all().order_by("order"),
        'reasonList':ReturnReason.objects.all().order_by("order"),
    })
def list_all_returned(request):
    try:
        returned_item_id = request.GET['returnedItemID']
        try:
            refunded_list = ReturnedItemDetails.objects.filter(id = int(returned_item_id))
        except:
            refunded_list = ReturnedItemDetails.objects.all()
    except:
        refunded_list = ReturnedItemDetails.objects.all()

    return render_response(request, 'rts/list_returned_items.html',{
        'refunded_list': refunded_list,
    })
def update_refunded_order(request):
    if request.method == 'POST':
        returnedItem = ReturnedItemDetails.objects.get(pk = int(request.POST['returnedItemID']))
        customerContacted = request.POST['customerContacted']
        refundReferenceNumber = request.POST['refundReferenceNumber']
        newCoupon = None
        newCoupon = request.POST['newCoupon']
        if newCoupon is not None and len(newCoupon)>0:
            try:
                refundedItem = RefundedItemDetails.objects.get(returned_item = returnedItem)
                refundedItem.new_coupon = newCoupon
                refundedItem.create_date = datetime.now()
                refundedItem.create_user = request.user
                refundedItem.status = rts_status.REFUNDED
                refundedItem.save()
            except:
                RefundedItemDetails.objects.create(returned_item = returnedItem, create_date = datetime.now(), create_user = request.user , status = rts_status.REFUNDED, customer_contacted = customerContacted, refund_reference_number = refundReferenceNumber, isCouponNeeded = True, new_coupon = newCoupon)
        else:
            try:
                isCouponNeeded = request.POST['isCouponNeeded']
                RefundedItemDetails.objects.create(returned_item = returnedItem, create_date = datetime.now(), create_user = request.user , status = rts_status.COUPON_PENDING, customer_contacted = customerContacted, refund_reference_number = refundReferenceNumber, isCouponNeeded = True )
            except:
                RefundedItemDetails.objects.create(returned_item = returnedItem, create_date = datetime.now(), create_user = request.user , status = rts_status.REFUNDED, customer_contacted = customerContacted, refund_reference_number = refundReferenceNumber, isCouponNeeded = False )
        return redirect('/rts/list_all_returned/?returnedItemID='+request.POST['returnedItemID'])

def update_returned_order(request):
    if request.method == 'POST':
        returnedOrder = OrderItemBaseForReturns.objects.get(id_sales_order_item = int(request.POST['returnedItemID']))
        returnReason = ReturnReason.objects.get(pk = int(request.POST['reasonList']))
        actionType = ActionType.objects.get(pk = int(request.POST['actionList']))
        comment = request.POST['comment']
        ReturnedItemDetails.objects.create(order_item = returnedOrder, return_reason = returnReason, action_type = actionType, comment = comment, create_user = request.user )
        return redirect('/rts/list_all/?suborder_nr='+returnedOrder.suborder_number+'&order_nr='+returnedOrder.order_nr)