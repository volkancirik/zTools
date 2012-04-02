# Create your views here.


from models import Order
from models import CrossStatus
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse

from django.http import HttpResponseRedirect


def order(request):

    if request.method == 'POST':
        keyword =  request.POST["keyword"]
        column_name=request.POST["column_name"]
        allOrders= Order.objects.all()
        if column_name == 'supplier_name':
          orders_dict = allOrders.filter(supplier_name__contains=keyword)
        orderList = list()

        for anOrder in orders_dict:
            orderList.append(anOrder)
        return render_to_response('orders.html', {'orders' : orderList},context_instance = RequestContext(request) )
    else:
        try:
            orders = Order.objects.all()
        except Order.DoesNotExist:
            raise Http404

        for anOrder in orders:
            try:
                statusForAnOrder = CrossStatus.objects.get( pk = anOrder.id)
                anOrder.status = statusForAnOrder.order_status
            except CrossStatus.DoesNotExist:
                statusForAnOrder = CrossStatus.objects.create(order_id = anOrder,order_status = 'Unprocessed')
                anOrder.status = 'Unprocessed'
    return render_to_response('orders.html', {'orders' : orders},context_instance = RequestContext(request) )

def updateOrder(request):


    orderIDs = list()
    orderIDs = request.POST.getlist('orderChecked')

    for anOrderID in orderIDs:
        try:
            anOrder = Order.objects.get(pk = int(anOrderID))
        except Order.DoesNotExist:
            raise Http404
        try:
            toBeUpdated = CrossStatus.objects.get(pk = anOrder.id)
        except CrossStatus.DoesNotExist:
            toBeUpdated = CrossStatus.objects.create(order_id = anOrder)
        toBeUpdated.order_status =  request.POST["status"]
        toBeUpdated.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def sort(request,criteria):

    if criteria == "order_id":
        orders = Order.objects.order_by('-order_number')
    if criteria == "barcode":
        orders = Order.objects.order_by('-barcode')
    if criteria == "quantity":
        orders = Order.objects.order_by('-quantity')
    for anOrder in orders:
        try:
            statusForAnOrder = CrossStatus.objects.get( pk = anOrder.id)
            anOrder.status = statusForAnOrder.order_status
        except CrossStatus.DoesNotExist:
            statusForAnOrder = CrossStatus.objects.create(order_id = anOrder,order_status = 'Unprocessed')
            anOrder.status = 'Unprocessed'
    return render_to_response('orders.html', {'orders' : orders},context_instance = RequestContext(request) )

def searchOrder(request,column_name):

    if request.method == 'POST':
        keyword =  request.POST["keyword"]
        column_name=request.POST["column_name"]
        allOrders= Order.objects.all()
        if column_name == 'supplier_name':
            orders_dict = allOrders.filter(supplier_name__contains=keyword)
        orderList = list()
        for anOrder in orders_dict:
            orderList.append(anOrder)
        return render_to_response('orders.html', {'orders' : orderList},context_instance = RequestContext(request) )
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def test(request):
    return render_to_response('jqueryTest.html',context_instance = RequestContext(request) )
