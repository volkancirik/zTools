from django.http import HttpResponse
from django.shortcuts import redirect
from acceptance.models import Shipment, ShipmentItem
from good_acc.acceptance.helper_functions import render_response
import csv

class Column():
    ID_SHIPMENT_ITEM = 0
    SHIPMENT_ID = 1
    BARCODE = 2
    SKU = 3
    QUANTITY = 4
    IMAGE_URL = 5

def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES["file"]
        data = csv.reader(file)
        fields = data.next()

        shipment = None
        for row in data:
            cols = row[0].split('\t')
            if shipment is None:
                shipment = Shipment()
                shipment.code = cols[Column.SHIPMENT_ID]
                shipment.save()

            si = ShipmentItem()
            si.code = int(cols[Column.ID_SHIPMENT_ITEM])
            si.barcode = cols[Column.BARCODE]
            si.sku = cols[Column.SKU]
            si.quantity = int(cols[Column.QUANTITY])
            si.photo_url = cols[Column.IMAGE_URL]
            si.shipment = shipment
            si.save()
            print si.pk

        return render_response(request, 'good_acc/item_view.html',{'sid':shipment.pk})

    return render_response(request, 'good_acc/upload_csv.html',{'error':request.GET.get("error",None)})

def item_view(request):
    sid = request.POST.get("sid",None)
    if sid is None:
        return redirect('/acceptance/upload_csv/?error=1')

    barcode = request.POST.get("barcode",None)

    isExists = False
    si = ShipmentItem()
    if barcode is not None:
        shipment = Shipment.objects.get(pk=int(sid))
        if shipment.shipmentitem_set.filter(barcode = barcode).count():
            si = shipment.shipmentitem_set.get(barcode = barcode)
            isExists = True

    return render_response(request, 'good_acc/item_view.html',{'si':si,'sid':sid,'isExists':isExists})

def action(request):
    type = request.GET.get("type")
    si_id = request.GET.get("siid")
    sid = request.GET.get("sid")

    si = ShipmentItem()
    if ShipmentItem.objects.filter(pk=int(si_id)).count():
        si = ShipmentItem.objects.get(pk=int(si_id))
    else:
        si.barcode = si_id
        si.shipment = Shipment.objects.get(pk=sid)

    if type == "1":
        si.quantity_received +=1
        if si.quantity_stocked == si.quantity:
            si.save()
            return HttpResponse("2", mimetype='application/json; charset=utf8')

        si.quantity_stocked += 1
    if type == "2":
        si.quantity_received +=1
        si.quantity_photomismatch += 1
    if type == "3":
        si.quantity_received +=1
        si.quantity_damaged += 1
    if type == "4":
        si.quantity_stocked -= 1
        si.quantity_received -=1
    if type == "5":
        si.quantity_photomismatch -= 1
        si.quantity_received -=1
    if type == "6":
        si.quantity_damaged -= 1
        si.quantity_received -=1

    si.save()
    return HttpResponse("1", mimetype='application/json; charset=utf8')