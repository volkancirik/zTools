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
import xlwt

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


    request.session.__delitem__("supplier")
    request.session.__delitem__("siList")
    request.session.__delitem__("shipment")

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
    writer.writerow(['id_shipment_item\tshipment_id\tbarcode\tsku\tquantity\timage_url\tbrand\tzidaya_name\tsize\tsupplier_color\tsku_supplier_simple\tsku_supplier_config'])

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
        sku = si.catalog_simple.sku
        icc = si.catalog_simple.id_catalog_config
        reverse_icc = str(icc)[::-1]
        image_url = 'http://static.zidaya.com/p/-'+reverse_icc+'-1-product.jpg'
        brand = str(si.catalog_simple.brand)
        zname = str(si.catalog_simple.zidaya_name)
        try:
            size = si.catalog_simple.simplessizes.size
        except:
            size = "yok"
        color = si.catalog_simple.supplier_color
        try:
            simple = str(si.catalog_simple.sku_supplier_simple)
        except:
            simple = "-"
        try:
            config = str(si.catalog_simple.sku_supplier_config)
        except:
            config = "-"

        writer.writerow([str(isi)+'\t'+str(sid)+'\t'+barcode+'\t'+sku+'\t'+str(si.quantity_ordered)+'\t'+image_url+'\t'+brand+'\t'+zname+'\t'+size+'\t'+color+'\t'+simple+'\t'+config])

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
def export_shipments_excel(request):
    shipments = Shipment.objects.all()
    #shipments = request.GET['slist']

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    field_names = ['status','number','supplier','shipment_type','is_consignment','totalShipmentItemCount','create_date','proposed_shipment_date','confirmed_shipment_date','date_received','comment','damaged_return_rate','cancel_reason','create_user','invoice_url']
    index_counter = 1


    for index_i,field in enumerate(field_names):
        sheet.write(0,index_i,[unicode(field).encode('utf-8') ])
        index_counter +=1

    for index_i,a_shipment in enumerate(shipments):
        for index_j,field in enumerate(field_names):
            if index_j == 3 :
                sheet.write(index_i+1,index_j,[unicode(a_shipment.shipmentType.name).encode('utf-8') ])
            elif index_j == 12:
                try:
                    sheet.write(index_i+1,index_j,[unicode(a_shipment.cancel_reason.name).encode('utf-8') ])
                except :
                    pass
            elif index_j == 13:
                try:
                    sheet.write(index_i+1,index_j,[unicode(a_shipment.create_user.email).encode('utf-8') ])
                except :
                    pass
            else:
                sheet.write(index_i+1,index_j,[unicode(getattr(a_shipment, field)).encode('utf-8') ])

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+'shipment'+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response

@login_required
@check_permission('Sms')
def export_a_shipment_excel(request):
    sid = request.GET.get("sid",None)
    if sid is  None or Shipment.objects.filter(pk=sid).count() == 0:
        return redirect("/sms/list_shipment/")

    shipment = Shipment.objects.get(pk=sid)
    siList = ShipmentItem.objects.filter(shipment=shipment)

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    field_names = ['quantity_ordered','sku','sku_config','cost','tax_percent','barcode_ean','barcode_to_export','brand','sku_supplier_config','sku_supplier_simple','zidaya_name','supplier_color','size','supplier_material','supplier_product_name']
    index_counter = 1

    for index_i,field in enumerate(field_names):
        sheet.write(0,index_i,[unicode(field).encode('utf-8') ])
        index_counter +=1

    for index_i,an_item in enumerate(siList):
        ics = CatalogSimple.objects.get(pk=an_item.catalog_simple.pk)
        for index_j,field in enumerate(field_names):
            if index_j == 0:
                sheet.write(index_i+1,index_j,[unicode(getattr(an_item, field)).encode('utf-8') ])
            elif index_j == 12:
                sheet.write(index_i+1,index_j,[unicode(ics.simplessizes.size).encode('utf-8') ])
            else:
                sheet.write(index_i+1,index_j,[unicode(getattr(ics, field)).encode('utf-8') ])

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+'shipment'+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response

@login_required
@check_permission('Sms')
def export_basket_excel(request):
    siList = request.session.get("siList",[])

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    field_names = ['quantity_ordered','sku','sku_config','cost','tax_percent','barcode_ean','barcode_to_export','brand','sku_supplier_config','sku_supplier_simple','zidaya_name','supplier_color','size','supplier_material','supplier_product_name']
    index_counter = 1

    for index_i,field in enumerate(field_names):
        sheet.write(0,index_i,[unicode(field).encode('utf-8') ])
        index_counter +=1

    for index_i,an_item in enumerate(siList):
        ics = CatalogSimple.objects.get(pk=an_item.catalog_simple.pk)
        for index_j,field in enumerate(field_names):
            if index_j == 0:
                try:
                    sheet.write(index_i+1,index_j,[unicode(getattr(an_item, field)).encode('utf-8') ])
                except :
                    pass
            elif index_j == 12:
                try:
                    sheet.write(index_i+1,index_j,[unicode(ics.simplessizes.size).encode('utf-8') ])
                except :
                    pass
            else:
                try:
                    sheet.write(index_i+1,index_j,[unicode(getattr(ics, field)).encode('utf-8') ])
                except :
                    pass

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+'shipment'+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response
