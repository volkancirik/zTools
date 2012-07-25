import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson
from cross_order.helper_functions import render_response
from cross_order.utils import check_permission
from sms.helper import getTotalShipmentItemCount, generateShipmentString
from sms.models import Supplier, CatalogSimple, CatalogSupplier, CatalogBrand, ShipmentItem, Shipment, ShipmentType, ShipmentStatus, SimpleStatus,SimpleShipmentTypeID, BrandStatus, SupplierStatus, CancellationReason

@login_required
@check_permission('Sms')
def list_catalog_simple(request):
    if request.method == 'POST' and request.POST["sid"]!= '-1':
        sup = None
        csList = CatalogSimple.objects.all()
        if "sid" in request.POST and CatalogSupplier.objects.filter(pk=request.POST["sid"]).count():
            sup = CatalogSupplier.objects.get(pk=request.POST["sid"])
            csList = CatalogSimple.objects.filter(supplier=sup,status_simple = SimpleStatus.ACTIVE, status_config = SimpleStatus.ACTIVE, id_shipment_type = SimpleShipmentTypeID.ON_WAREHOUSE, brand__status = BrandStatus.ACTIVE)

        return render_response(request, 'sms/list_catalog_simple.html',
                {
                    'supplier':sup,
                    'csList':csList,
                    'supList':CatalogSupplier.objects.filter( status = SupplierStatus.ACTIVE).order_by('name'),
                    'totalShipmentItemCount':getTotalShipmentItemCount(request)
                })
    else:

        return render_response(request, 'sms/list_catalog_simple.html',
                {
                    'supList':CatalogSupplier.objects.filter( status = SupplierStatus.ACTIVE).order_by('name'),
                    'totalShipmentItemCount':getTotalShipmentItemCount(request)
                })

@login_required
@check_permission('Sms')
def update_basket(request):
    ics = request.POST.get("id_catalog_simple",None)
    count = request.POST.get("count",0)

    totalCount = 0
    currentBasketSize = getTotalShipmentItemCount(request)

    shipment = request.session.get("shipment",Shipment())
    siList = request.session.get("siList",[])

    cs = CatalogSimple.objects.get(pk=ics)
    supplier = cs.supplier.pk

    if not currentBasketSize>0:
        request.session["supplier"] = supplier

    if supplier == request.session["supplier"]:
        si= ShipmentItem()
        si.catalog_simple = cs
        si.quantity_ordered = int(count)
        si.shipment = shipment
        si.catalog_simple = cs

        index = -1
        for item in siList:
            if item.catalog_simple == cs:
                item.quantity_ordered += int(count)
                index = siList.index(item)
                break

        if index < 0:
            siList.append(si)

        request.session["shipment"] = shipment
        request.session["siList"] = siList

        totalCount = getTotalShipmentItemCount(request)
    else:
        totalCount = -1

    json_models = simplejson.dumps(totalCount)
    return HttpResponse(json_models, mimetype='application/json; charset=utf8')

@login_required
@check_permission('Sms')
def view_basket(request):
    shipment = request.session.get("shipment",None)
    siList = request.session.get("siList",[])
    return render_response(request, 'sms/view_basket.html',
                {
                    'shipment':shipment,
                    'siList':siList,
                    'shipmentTypeList':ShipmentType.objects.all().order_by("order"),
                    'totalShipmentItemCount':getTotalShipmentItemCount(request)
                })

@login_required
@check_permission('Sms')
def delete_shipment_item(request):
    ics = request.GET.get("id_catalog_simple",None)

    cs = None
    if ics is not None and CatalogSimple.objects.filter(pk=ics).count():
        cs = CatalogSimple.objects.get(pk=ics)

    if cs is not None:
        siList = request.session.get("siList",[])
        counter = 0
        for item in siList:
            if item.catalog_simple == cs:
                siList.__delitem__(counter)
                request.session["siList"] = siList
                break
            counter += 1

    return redirect('/sms/view_basket/')

@login_required
@check_permission('Sms')
def create_shipment(request):
    if request.method == 'POST':

        date = datetime.datetime.now()
        try:
            date =  datetime.datetime.strptime(request.POST['proposedShipmentDate'], "%m/%d/%Y")
        except:
            pass

        shipmentType = ShipmentType.objects.get(pk = int(request.POST['stList']))

        shipment = request.session.get("shipment",Shipment())
        shipment.shipmentType = shipmentType
        shipment.is_consignment = request.POST.get("isConsignment",False)
        shipment.create_user = request.user
        shipment.update_user = request.user
        shipment.proposed_shipment_date = date
        shipment.number = generateShipmentString()

        shipment.supplier = request.session.get("siList")[0].catalog_simple.supplier

        shipment.comment = request.POST['comment']
        shipment.damaged_return_rate = request.POST['damagedReturnRate']
        shipment.save()

        totalCount = 0
        for si in request.session.get("siList",[]):
            si.shipment = shipment
            totalCount += si.quantity_ordered
            si.save()

        shipment.totalShipmentItemCount = totalCount
        shipment.save()

        request.session.__delitem__("shipment")
        request.session.__delitem__("siList")
    
        return redirect('/sms/list_shipment/')
    else:
        return redirect('/sms/view_basket/')

@login_required
@check_permission('Sms')
def list_shipment(request):
    shipmentList = Shipment.objects.all().order_by("-create_date")
    return render_response(request, 'sms/list_shipment.html',
                {
                    'shipmentList':shipmentList,
                    'totalShipmentItemCount':getTotalShipmentItemCount(request),
                })

@login_required
@check_permission('Sms')
def view_shipment(request):
    sid = request.GET.get("sid",None)
    if sid is  None or Shipment.objects.filter(pk=sid).count() == 0:
        return redirect("/sms/list_shipment/")

    shipment = Shipment.objects.get(pk=sid)
    siList = ShipmentItem.objects.filter(shipment=shipment)

    return render_response(request, 'sms/view_shipment.html',
                {
                    'shipment':shipment,
                    'siList':siList,
                    'totalShipmentItemCount':getTotalShipmentItemCount(request),
                    'cancelTypeList' :CancellationReason.objects.all().order_by("order"),
                })

@login_required
@check_permission('Sms')
def confirm_shipment(request):
    shipment = Shipment.objects.get(pk=request.POST['sid'])

    shipment.status = ShipmentStatus.CONFIRMED
    shipment.update_user = request.user
    shipment.update_date = datetime.datetime.now()

    shipment.confirmed_shipment_date = datetime.datetime.strptime(request.POST['confirmedShipmentDate'], "%m/%d/%Y")
    shipment.comment = request.POST['comment']
    shipment.save()
    
    return redirect('/sms/list_shipment/')

@login_required
@check_permission('Sms')
def comment_on_shipment(request):
    shipment = Shipment.objects.get(pk=request.POST['sid'])
    shipment.comment = request.POST['comment']
    shipment.save()
    return redirect('/sms/list_shipment/')


@login_required
@check_permission('Sms')
def cancel_shipment(request):
    shipment = Shipment.objects.get(pk=request.POST['sid'])
    shipment.status = ShipmentStatus.DENIED_BY_OPS
    if request.user.groups.filter(name='SmsWarehouse').count() > 0:
        shipment.status = ShipmentStatus.DENIED_BY_WH
    shipment.update_user = request.user
    shipment.update_date = datetime.datetime.now()

    cancel = CancellationReason.objects.get(pk = request.POST['cancelList'])
    shipment.cancel_reason = cancel
    shipment.comment = request.POST['comment']

    shipment.save()

    return redirect('/sms/list_shipment/')

@login_required
@check_permission('SmsWarehouse')
def receive_shipment(request):
    shipment = Shipment.objects.get(pk=request.GET['sid'])
    shipment.status = ShipmentStatus.RECEIVED
    shipment.update_user = request.user
    shipment.update_date = datetime.datetime.now()
    shipment.save()

    return redirect('/sms/list_shipment/')