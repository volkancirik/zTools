from datetime import  datetime,time,timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
#from dms.forms import DocumentUploadForm
from cross_order.utils import check_permission
from cts.models import CancelItemDetails, CancelReason, OrderItemBaseForCancellation
from settings import MEDIA_ROOT, LOGIN_URL

@login_required
def cancel_item(request):
    oii = request.GET.get('order_item_id','')   #order item id

    dict = {
        'reasonList':CancelReason.objects.all().order_by("order"),
        'suborder_nr':oii
    }

    if request.method == 'GET' and oii != '':
        cri = request.GET.get('cancelReason','')
        oib = OrderItemBaseForCancellation.objects.get(id_sales_order_item = int(oii) )
        cr = CancelReason.objects.get(pk = int(cri) )
        cid = CancelItemDetails()
        cid.order_item = oib
        cid.cancel_reason = cr
        cid.create_user = request.user
        cid.create_date = datetime.now()
        cid.save()

    return render_response(request, 'cts/home_cancellation.html',dict)

@login_required
def cancel_mass(request):

    dict = {
        'reasonList':CancelReason.objects.all().order_by("order")
    }

    if request.method == 'POST':
         order_item = request.POST['order_item']
         order_item_list = order_item.split("\r\n")

         for oi in order_item_list:
             oi = oi.lstrip().rstrip()
             cri = request.POST.get('cancelReason')
             oib = OrderItemBaseForCancellation.objects.get(id_sales_order_item = int(oi) )
             cr = CancelReason.objects.get(pk = int(cri) )
             cid = CancelItemDetails()
             cid.order_item = oib
             cid.cancel_reason = cr
             cid.create_user = request.user
             cid.create_date = datetime.now()
             cid.save()

    return render_response(request, 'cts/mass_cancel.html',dict)