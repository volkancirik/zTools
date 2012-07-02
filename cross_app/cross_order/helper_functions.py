import datetime
import random
from string import split
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
import xlwt

def getOrderSearchQuery(form):
    cross_status = form.cleaned_data['cross_status']
    order_item_id = form.cleaned_data['order_item_id']
    zidaya_order_item = form.cleaned_data['zidaya_order_item']
    sku = form.cleaned_data['sku']
    suborder_number = form.cleaned_data['suborder_number']
    supplier_name = form.cleaned_data['supplier_name']
    attribute_set = form.cleaned_data['attribute_set']
    supplier_sku_config = form.cleaned_data['supplier_sku_config']
    supplier_sku_simple = form.cleaned_data['supplier_sku_simple']
    barcode = form.cleaned_data['barcode']
    name = form.cleaned_data['name']
    comment = form.cleaned_data['comment']
    inbound_order_number = form.cleaned_data['inbound_order_number']
    order_date_start = form.cleaned_data['order_date_start']
    order_date_end = form.cleaned_data['order_date_end']
    supplier_order_date_start = form.cleaned_data['supplier_order_date_start']
    supplier_order_date_end = form.cleaned_data['supplier_order_date_end']
    last_update_date_start = form.cleaned_data['last_update_date_start']
    last_update_date_end = form.cleaned_data['last_update_date_end']

    q = Q()
    if cross_status is not None:
        q.add(Q(ordercrossdetails__cross_status=cross_status), Q.AND)
    if attribute_set is not None:
        q.add(Q(ordercrossdetails__order_attribute=attribute_set.attributeCode), Q.AND)
    if order_item_id != "":
        q.add(Q(id_sales_order_item__icontains=order_item_id), Q.AND)
    if zidaya_order_item != "":
        q.add(Q(order_nr__icontains=zidaya_order_item), Q.AND)
    if sku != "":
        q.add(Q(sku__icontains=sku), Q.AND)
    if supplier_name != "":
        q.add(Q(supplier__name__icontains=supplier_name), Q.AND)
    if supplier_sku_config != "":
        q.add(Q(sku_supplier_config__icontains=supplier_sku_config), Q.AND)
    if supplier_sku_simple != "":
        q.add(Q(sku_supplier_simple__icontains=supplier_sku_simple), Q.AND)
    if barcode != "":
        q.add(Q(barcode_ean__icontains=barcode), Q.AND)
    if name != "":
        q.add(Q(name__icontains=name), Q.AND)
    if comment != "":
        q.add(Q(ordercrossdetails__comment__icontains=comment), Q.AND)
    if inbound_order_number != "":
        q.add(Q(ordercrossdetails__inbound_order_number__icontains=inbound_order_number), Q.AND)
    if order_date_start != "":
        order_date_start = datetime.datetime.strptime(order_date_start, "%m/%d/%Y")
        order_date_start = datetime.datetime.combine(order_date_start, datetime.time.min)
        q.add(Q(order_date__gte=order_date_start), Q.AND)
    if order_date_end != "":
        order_date_end = datetime.datetime.strptime(order_date_end, "%m/%d/%Y")
        order_date_end = datetime.datetime.combine(order_date_end, datetime.time.max)
        q.add(Q(order_date__lte=order_date_end), Q.AND)
    if supplier_order_date_start != "":
        supplier_order_date_start = datetime.datetime.strptime(supplier_order_date_start, "%m/%d/%Y")
        supplier_order_date_start = datetime.datetime.combine(supplier_order_date_start, datetime.time.min)
        q.add(Q(ordercrossdetails__supplier_order_date__gte=supplier_order_date_start), Q.AND)
    if supplier_order_date_end != "":
        supplier_order_date_end = datetime.datetime.strptime(supplier_order_date_end, "%m/%d/%Y")
        supplier_order_date_end = datetime.datetime.combine(supplier_order_date_end, datetime.time.max)
        q.add(Q(ordercrossdetails__supplier_order_date__lte=supplier_order_date_end), Q.AND)
    if last_update_date_start != "":
        last_update_date_start = datetime.datetime.strptime(last_update_date_start, "%m/%d/%Y")
        last_update_date_start = datetime.datetime.combine(last_update_date_start, datetime.time.min)
        q.add(Q(lastupdate__update_date__gte=last_update_date_start), Q.AND)
    if last_update_date_end != "":
        last_update_date_end = datetime.datetime.strptime(last_update_date_end, "%m/%d/%Y")
        last_update_date_end = datetime.datetime.combine(last_update_date_end, datetime.time.max)
        q.add(Q(lastupdate__update_date__lte=last_update_date_end), Q.AND)
    return q

def modelToExcel(data,field_names,file_name):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    index_counter = 1
    for index_i,field in enumerate(field_names):
         sheet.write(0,index_i,[unicode(field).encode('utf-8') ])
         index_counter +=1

    for index_i,an_order in enumerate(data):
        for index_j,field in enumerate(field_names):
            sheet.write(index_i+1,index_j,[unicode(getattr(an_order, field)).encode('utf-8') ])

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+file_name+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

def convertDatetimeToString(o):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    if isinstance(o, datetime.date):
        return o.strftime(DATE_FORMAT)
    elif isinstance(o, datetime.time):
        return o.strftime(TIME_FORMAT)
    elif isinstance(o, datetime.datetime):
        return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))

def acronym(phrase):
    result = ""
    for word in split(phrase):
        result += word[0].upper()
    return slugify(result)

def generateTransactionString(supplier_name):
    today = convertDatetimeToString(datetime.datetime.today())
    number = str(random.randint(0,9999))

    #number yerine id, acronym yerine supplier table'dan abbreviation gelecek!
    transaction_string = 'TR'  + today + '-' + acronym(supplier_name) + '-' + number
    return transaction_string

def getTodayAsString():
    today = datetime.datetime.now()
    return str(today.year) +"_"+ str(today.month).zfill(2) +"_"+ str(today.day).zfill(2) +"_"+ str(today.hour).zfill(2) +"_"+ str(today.minute).zfill(2)