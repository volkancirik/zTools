import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson
from cross_order.helper_functions import render_response
from cross_order.utils import check_permission
from sms.helper import getTotalShipmentItemCount, generateShipmentString
from sms.models import Supplier, CatalogSimple, CatalogSupplier, CatalogBrand, ShipmentItem, Shipment, ShipmentType, ShipmentStatus, SimpleStatus,SimpleShipmentTypeID, BrandStatus, SupplierStatus, CancellationReason
import csv

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


    json_models = simplejson.dumps(totalCount)
    return HttpResponse(json_models, mimetype='application/json; charset=utf8')

@login_required
@check_permission('Sms')
def clone_shipment(request):

    sid = request.POST.get("sid")
    shipment = Shipment.objects.get(pk = sid)

    try:
        request.session.__delitem__("supplier")
    except:
        pass
    try:
        request.session.__delitem__("siList")
    except :
        pass
    try:
        request.session.__delitem__("shipment")
    except :
        pass

    request.session["supplier"] = shipment.supplier.pk
    siListQuerySet = ShipmentItem.objects.filter( shipment = shipment)
    siList = list()
    for si in siListQuerySet:
        siList.append(si)
    request.session["siList"] = siList
    request.session["shipment"] = Shipment()

    totalCount = getTotalShipmentItemCount(request)
    json_models = simplejson.dumps(totalCount)
    return HttpResponse(json_models, mimetype='application/json; charset=utf8')


@login_required
@check_permission('Sms')
def check_basket(request):
    ics = request.POST.get("id_catalog_simple",None)
    count = request.POST.get("count",0)

    result = 0
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
                result = item.quantity_ordered
                index = siList.index(item)
                break

        if index < 0:
            result = -2
    else:
        result = -1

    json_models = simplejson.dumps(result)
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

@login_required
@check_permission('SmsWarehouse')
def export_shipment_csv(request):
    sid = request.GET.get("sid",None)
    if sid is  None or Shipment.objects.filter(pk=sid).count() == 0:
        return redirect("/sms/list_shipment/")

    shipment = Shipment.objects.get(pk=sid)
    filename = shipment.number
    siList = ShipmentItem.objects.filter(shipment=shipment)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+filename+'.csv'

    writer = csv.writer(response)
    writer.writerow(['id_shipment_item\tshipment_id\tbarcode\tsku\tquantity\timage_url'])

    for si in siList:
        isi = si.pk
        sid = si.shipment_id
        #check for which field to be used for barcode
        if si.catalog_simple.id_barcode_to_export == 1:
            barcode = si.catalog_simple.barcode_ean
        elif si.catalog_simple.id_barcode_to_export == 2:
            skuSplitter = si.catalog_simple.sku.split('-')
            barcode = skuSplitter[0]
        elif si.catalog_simple.id_barcode_to_export == 3:
            if not si.catalog_simple.barcode_ean == None:
                barcode = si.catalog_simple.barcode_ean
            else:
                barcode = si.catalog_simple.sku.replace('-','')
        else:
            pass

        #create image url for product
        icc = si.catalog_simple.id_catalog_config
        reverse_icc = str(icc)[::-1]
        image_url = 'http://static.zidaya.com/p/-'+reverse_icc+'-1-product.jpg'

        writer.writerow([str(isi)+'\t'+str(sid)+'\t'+barcode+'\t'+si.catalog_simple.sku+'\t'+str(si.quantity_ordered)+'\t'+image_url])

    return response


@login_required
@check_permission('Sms')
def add_invoice(request):
    if request.method == 'POST':
        try:
            snr = request.POST['shipmentNr']
            s_url = request.POST['shipmentInvoiceUrl']
            shipment = Shipment.objects.get(number = snr )
            shipment.invoice_url = s_url
            shipment.save()
        except:
            pass

    return redirect('/sms/list_shipment/')

@login_required
@check_permission('Sms')
def import_mass(request):
    if request.method == 'POST':
        sku_simple = request.POST['sku_simple']
        sku_quantity = request.POST['sku_simple_quantity']
        sup = None
        if "sid" in request.POST and CatalogSupplier.objects.filter(pk=request.POST["sid"]).count():
            sup = CatalogSupplier.objects.get(pk=request.POST["sid"])

        shipment = Shipment()
        siList = []
        exceptionList = []

        sku_simple_list = sku_simple.split("\r\n")
        quantity_list = sku_quantity.split("\r\n")
        index = 0
        for sku in sku_simple_list:
            sku = sku.lstrip().rstrip()
            if sku == "":
                continue
            if not CatalogSimple.objects.filter(sku=sku).count():
                exception = [sku,1]
                exceptionList.append(exception)
            elif not CatalogSimple.objects.filter(sku=sku,supplier = sup).count():
                exception = [sku,2]
                exceptionList.append(exception)
            elif not CatalogSimple.objects.filter(sku=sku,supplier = sup,status_simple = SimpleStatus.ACTIVE).count():
                exception = [sku,3]
                exceptionList.append(exception)
            elif not CatalogSimple.objects.filter(sku=sku,supplier = sup,status_simple = SimpleStatus.ACTIVE,status_config = SimpleStatus.ACTIVE).count():
                exception = [sku,4]
                exceptionList.append(exception)
            elif not CatalogSimple.objects.filter(sku=sku,supplier = sup,status_simple = SimpleStatus.ACTIVE,status_config = SimpleStatus.ACTIVE,id_shipment_type = SimpleShipmentTypeID.ON_WAREHOUSE).count():
                exception = [sku,5]
                exceptionList.append(exception)
            elif not quantity_list[index].isdigit():
                exception = [sku,6]
                exceptionList.append(exception)
            elif not CatalogSimple.objects.filter(sku=sku,
                                            supplier = sup,
                                            status_simple = SimpleStatus.ACTIVE,
                                            status_config = SimpleStatus.ACTIVE,
                                            id_shipment_type = SimpleShipmentTypeID.ON_WAREHOUSE,
                                            brand__status = BrandStatus.ACTIVE).count() > 0:
                exception = [sku,7]
                exceptionList.append(exception)
            else:
                cs = CatalogSimple.objects.get(sku=sku)
                si= ShipmentItem()
                si.catalog_simple = cs
                si.quantity_ordered = int(quantity_list[index])
                si.shipment = shipment
                siList.append(si)

            index +=1

        if not exceptionList:
            request.session["shipment"] = shipment
            request.session["siList"] = siList
            return redirect('/sms/view_basket/')
        else:
            return render_response(request, 'sms/import_mass.html',
                {
                    'supList':CatalogSupplier.objects.filter( status = SupplierStatus.ACTIVE).order_by('name'),
                    'exceptionList': exceptionList ,
                    'exceptionListLength':len(exceptionList),
                    'sku_simple':request.POST['sku_simple'],
                    'sku_quantity':request.POST['sku_simple_quantity'],
                    'supplier':sup,
                    'totalShipmentItemCount':getTotalShipmentItemCount(request)
                })
    else:
        return render_response(request, 'sms/import_mass.html',
                {
                    'supList':CatalogSupplier.objects.filter( status = SupplierStatus.ACTIVE).order_by('name'),
                    'exceptionList' : [],
                    'totalShipmentItemCount':getTotalShipmentItemCount(request)
                })
