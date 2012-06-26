import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models.query_utils import Q
from django.db.transaction import Transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
import xlwt
from cross_order.forms import OrderSearchForm
from cross_order.helper_functions import render_response, generateTransactionString, modelToExcel, getOrderSearchQuery
from cross_order.models import Supplier, CrossStatus, Order, LastUpdate, Transactions, OrderTransaction, OrderCrossDetails, OrderAttributeSet, TransactionStatus, ReportConfirmedSkuBase, ReportConfirmedSupplierBase, ReportOutOfStockCrossDock, ReportUnprocessedCrossDock, OverdueCrossDock, ReportSql2Excel, ColumnType
from django.core.serializers.json import Serializer, DjangoJSONEncoder
from django.db import transaction, connection
from cross_order.utils import get_datatables_records

@login_required
def order_search_ajax(request):
    columnIndexNameMap = {
        0:'pk',
        1:'ordercrossdetails__cross_status__name',
        2:'supplier__name',
        3:'id_sales_order_item',
        4:'order_nr',
        5:'suborder_number',
        6:'sku',
        7:'size',
        8:'sku_supplier_simple',
        9:'sku_supplier_config',
        10:'barcode_ean',
        11:'name',
        12:'paid_price',
        13:'cost',
        14:'order_date',
        15:'ordercrossdetails__order_attribute',
        16:'ordercrossdetails__inbound_order_number',
        17:'ordercrossdetails__comment',
        18:'ordercrossdetails__supplier_order_date',
        #19:'lastupdate__update_date',
        }
    return get_datatables_records(request,
                                  Order.objects.values(
                                      'pk',
                                      'ordercrossdetails__cross_status__name',
                                      'id_sales_order_item',
                                      'order_nr',
                                      'suborder_number',
                                      'sku',
                                      'size',
                                      'sku_supplier_simple',
                                      'sku_supplier_config',
                                      'barcode_ean',
                                      'name',
                                      'paid_price',
                                      'cost',
                                      'order_date',
                                      'ordercrossdetails__order_attribute',
                                      'ordercrossdetails__inbound_order_number',
                                      'ordercrossdetails__comment',
                                      'ordercrossdetails__supplier_order_date',
                                      #'lastupdate__update_date',
                                      'supplier__name'
                                      ).all(),columnIndexNameMap)

@login_required
def order_search(request):
    form = OrderSearchForm()
    return render_response(request, 'cross_order/order_search.html',{'form':form,'crossList':CrossStatus.objects.all(),'attributeList':OrderAttributeSet.objects.all()})

@login_required
def report_list(request):
    return render_response(request, 'cross_order/report_list.html',{'report_list':ReportSql2Excel.objects.filter(isActive=True).order_by('order')})


@login_required
def get_excel_report(request):
    rep = ReportSql2Excel.objects.get(pk=request.GET["report"])
    cursor = connection.cursor()

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    index_counter = 0
    for field in rep.sql2excelcolumn_set.all():
         sheet.write(0,index_counter,[unicode(field.name).encode('utf-8') ])
         index_counter +=1


    query = "SELECT "
    for col in rep.sql2excelcolumn_set.all():
        query += (col.name + ",")

    query = query[0:len(query)-1]
    query += " FROM "
    query += rep.tb_name.replace('\'','')

    cursor.execute(query)
    index_i = 1
    for row in cursor.fetchall():
        index_j = 0
        for col in rep.sql2excelcolumn_set.all():
            if col.type == ColumnType.CHAR:
                sheet.write(index_i,index_j,[unicode(row[index_j]).encode('utf-8') ])
            elif col.type == ColumnType.FLOAT:
                sheet.write(index_i,index_j,Decimal(row[index_j]))
            elif col.type == ColumnType.INT:
                sheet.write(index_i,index_j,int(row[index_j]))
            index_j += 1
        index_i += 1

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+rep.excel_name+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response


@login_required
def list_supplier(request):

    start_date = datetime.datetime.now()
    start_date = datetime.datetime.combine(start_date, datetime.time.min)

    end_date = datetime.datetime.now()
    if "dateStart" in request.POST:
        start_date = datetime.datetime.strptime(request.POST['dateStart'], "%m/%d/%Y")
    if "dateEnd" in request.POST:
        end_date = datetime.datetime.strptime(request.POST['dateEnd'], "%m/%d/%Y")
        end_date = datetime.datetime.combine(end_date, datetime.time.max)

    oa = None
    cs = CrossStatus.objects.all().order_by("order")[0]
    supList = []

    try:
        oa = OrderAttributeSet.objects.get(pk = int(request.POST['attributeFilter']))
        for s in Supplier.objects.all().order_by("name"):
            if s.order_set.filter(order_date__range=[start_date, end_date],ordercrossdetails__order_attribute = oa.attributeCode).count() >0:
                s.unprocessedCount = s.order_set.filter(ordercrossdetails__cross_status=cs,ordercrossdetails__order_attribute = oa.attributeCode,order_date__range=[start_date, end_date]).count()
                s.totalCount = s.order_set.filter(ordercrossdetails__order_attribute = oa.attributeCode,order_date__range=[start_date, end_date]).count()
                supList.append(s)
    except:
        for s in Supplier.objects.all().order_by("name"):
            if s.order_set.filter(order_date__range=[start_date, end_date]).count() >0:
               s.unprocessedCount = s.order_set.filter(ordercrossdetails__cross_status=cs,order_date__range=[start_date, end_date]).count()
               s.totalCount = s.order_set.filter(order_date__range=[start_date, end_date]).count()
               supList.append(s)

#   below is the older version of filterin suppliers
#    for s in Supplier.objects.all().order_by("name"):
#        if s.order_set.filter(order_date__range=[start_date, end_date]).count() >0:
#            s.unprocessedCount = s.order_set.filter(ordercrossdetails__cross_status=cs,order_date__range=[start_date, end_date]).count()
#            s.totalCount = s.order_set.filter(order_date__range=[start_date, end_date]).count()
#            supList.append(s)


    return render_response(request, 'cross_order/list_supplier.html',
            {
                'supList':supList,
                'start_date':start_date,
                'end_date':end_date,
                'attributeList':OrderAttributeSet.objects.all().order_by("order"),
                'oattribute':oa
            })

@login_required
def list_order(request):

    if "sid" not in request.GET or Supplier.objects.filter(pk=request.GET["sid"]).count() == 0 :
        return redirect('/cross_order/list_supplier/')

    cs = None
    oa = None
    try:
        cs = CrossStatus.objects.get(pk = int(request.GET['cstatus']))
    except:
        pass

    try:
        oa = OrderAttributeSet.objects.get(pk = int(request.GET['oattributeid']))
    except:
        pass

    sup = Supplier.objects.get(pk=request.GET["sid"])
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()
    if "dateStart" in request.GET:
        start_date = datetime.datetime.strptime(request.GET['dateStart'], "%m/%d/%Y")
    if "dateEnd" in request.GET:
        end_date = datetime.datetime.strptime(request.GET['dateEnd'], "%m/%d/%Y")
        end_date = datetime.datetime.combine(end_date, datetime.time.max)


    current_url = '/cross_order/list_order/?sid='+request.GET["sid"]+"&dateStart="+request.GET['dateStart']+"&dateEnd="+request.GET['dateEnd']+'&cstatus='
    orderList = sup.order_set.filter(order_date__range=(start_date,end_date))
    if cs is not None:
        orderList = orderList.filter(ordercrossdetails__cross_status=cs)
    if oa is not None:
        orderList = orderList.filter(ordercrossdetails__order_attribute = oa.attributeCode)

    return render_response(request, 'cross_order/list_order.html',
            {
                'supplier':sup,
                'start_date':start_date,
                'end_date':end_date,
                'orderList':orderList,
                'crossStatusList':CrossStatus.objects.all().order_by("order"),
                'current_url':current_url,
                'cstatus':cs,
                'oattribute':oa,
            })

@login_required
def update_transaction_status(request):
    trans_id_list = request.POST.getlist('transChecked')
    if not len(trans_id_list) or "buttonSource" not in request.POST:
        return redirect('/cross_order/transaction_list/')

    action = request.POST['buttonSource']
    if action == "status" and request.POST['statusUpdate'] is 0:
        return redirect('/cross_order/transaction_list/')

    if action == "status":
        for tid in trans_id_list:
            t = Transactions.objects.get(pk=tid)
            ts = TransactionStatus.objects.get(pk=request.POST['statusUpdate'])
            t.status = ts
            t.save()

    return redirect('/cross_order/transaction_list/?status='+request.GET['status'])


@login_required
def update_order_list(request):
    order_id_list = request.POST.getlist('orderChecked')
    if not len(order_id_list) or "buttonSource" not in request.POST:
        return redirect('/cross_order/list_order/')

    action = request.POST['buttonSource']
    if action == "status" and request.POST['statusUpdate'] is 0:
        return redirect('/cross_order/list_order/')
    if action == "inbound" and request.POST['inbound_order_number'] == "":
        return redirect('/cross_order/list_order/')
    if action == "comment" and request.POST['comment'] == "":
        return redirect('/cross_order/list_order/')

    if action == "status":
        cs = CrossStatus.objects.get(pk = request.POST['statusUpdate'])


        trans = Transactions()
        if cs.isTransactionGenerate:
            trans.code = generateTransactionString(Supplier.objects.get(pk=request.GET['sid']).name)
            trans.create_date = datetime.datetime.now()
            trans.create_user = request.user
            trans.status = TransactionStatus.objects.all().order_by("order")[0]
            trans.save()

        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.cross_status = cs
            o.ordercrossdetails.save()
            lu = LastUpdate()
            lu.update_date = datetime.datetime.now()
            lu.cross_status = cs
            lu.order = o
            lu.user = request.user
            lu.save()
            if cs.isTransactionGenerate:
                o.ordercrossdetails.supplier_order_date = datetime.datetime.now()
                o.ordercrossdetails.save()
                OrderTransaction.objects.create(trans = trans,order = o)

    elif action == "inbound":
        ion = request.POST['inbound_order_number']
        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.inbound_order_number = ion
            o.ordercrossdetails.save()
            
    elif action == "comment":
        comment = request.POST['comment']
        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.comment = comment
            o.ordercrossdetails.save()

    sid = request.GET['sid']
    dateStart = request.GET['dateStart']
    dateEnd = request.GET['dateEnd']
    return redirect('/cross_order/list_order/?sid='+sid+"&dateStart="+dateStart+"&dateEnd="+dateEnd+"&oattributeid="+request.GET['oattributeid'])

@login_required
def transaction_list(request):

    status = None
    try:
        status = TransactionStatus.objects.get(pk = int(request.GET['status']))
    except:
        if request.GET.get('status','') == "":
            status = TransactionStatus.objects.all().order_by("order")[0]

    current_url = '/cross_order/transaction_list/?status='
    tList = Transactions.objects.order_by('-create_date')
    if status is not None:
        tList = tList.filter(status = status)

    return render_response(request, 'cross_order/list_transaction.html',
            {
                'transList':tList,
                'statusList':TransactionStatus.objects.all().order_by("order"),
                'current_url':current_url,
                'status':request.GET.get('status','1')
            })

@login_required
def transaction_details(request,code):
    cs = None
    try:
        cs = CrossStatus.objects.get(pk = int(request.GET['cstatus']))
    except:
        pass

    orderList = OrderTransaction.objects.filter(trans__code=code)
    if cs is not None:
        orderList = orderList.filter(order__ordercrossdetails__cross_status=cs)

    return render_response(request, 'cross_order/list_transaction_details.html',
            {
                'orderTransactionList': orderList,
                'crossStatusList':CrossStatus.objects.all().order_by("order"),
                'code':code,
                'cstatus':cs,
                'trans':Transactions.objects.get(code=code)
            })

@login_required
def update_trans_order_list(request):
    order_id_list = request.POST.getlist('orderChecked')
    if not len(order_id_list) or "buttonSource" not in request.POST:
        return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')

    action = request.POST['buttonSource']
    if action == "status" and request.POST['statusUpdate'] is 0:
        return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')
    if action == "inbound" and request.POST['inbound_order_number'] == "":
        return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')
    if action == "comment" and request.POST['comment'] == "":
        return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')

    if action == "status":
        cs = CrossStatus.objects.get(pk = request.POST['statusUpdate'])
        if cs.isTransactionGenerate:
            return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')

        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.cross_status = cs
            o.ordercrossdetails.save()
            lu = LastUpdate()
            lu.update_date = datetime.datetime.now()
            lu.cross_status = cs
            lu.order = o
            lu.user = request.user
            lu.save()

    elif action == "inbound":
        ion = request.POST['inbound_order_number']
        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.inbound_order_number = ion
            o.ordercrossdetails.save()
    elif action == "comment":
        comment = request.POST['comment']
        for oid in order_id_list:
            o = Order.objects.get(pk=oid)
            o.ordercrossdetails.comment = comment
            o.ordercrossdetails.save()

    return redirect('/cross_order/transaction_details/'+request.GET['code']+'/')

#TODO
#@login_required
#def order_history(request):
#    if "pk" not in request.GET:
#        return ""
#    o = Order.objects.get(id=request.GET["pk"])
#    items_list = list(o.lastupdate_set.all().values())
#    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
#
#
#    return HttpResponse(simplejson.dumps(items_list,default=dthandler),'application/json')

@csrf_exempt
def order_history(request):
    if "pk" not in request.GET:
        return ""
    o = Order.objects.get(id=request.GET["pk"])

    data=""
    for i in o.lastupdate_set.all():
        data = data + i.user.email + "," + str(i.update_date) + "," + i.cross_status.name + ","

    data = data[:len(data)-1]

    return HttpResponse(data,'text/plain')


@login_required
def exportExcelOrders(request):
    supplier=None
    start_date = ""
    end_date = ""
    cs = None

    if "sup" in request.GET:
        supplier = Supplier.objects.get(pk=request.GET['sup'])
    if "startdate" in request.GET:
        start_date = datetime.datetime.strptime(request.GET['startdate'], "%m/%d/%Y")
    if "enddate" in request.GET:
        end_date = datetime.datetime.strptime(request.GET['enddate'], "%m/%d/%Y")
        end_date = datetime.datetime.combine(end_date, datetime.time.max)

    try:
        cs = CrossStatus.objects.get(pk = int(request.GET['cstatus']))
    except:
        pass

    orders = Order.objects.filter(supplier=supplier,order_date__range =[start_date,end_date])
    if cs is not None:
        orders = orders.filter(ordercrossdetails__cross_status=cs)

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    field_names = ['id_sales_order_item','order_nr','size','sku','sku_supplier_config','sku_supplier_simple','barcode_ean','name','status','suborder_number','paid_price','cost','tax_percent','tax_amount','order_date']
    cross_status_fields = ['order_attribute','inbound_order_number','supplier_order_date',]
    order_cross_details_fields = ['name']

    index_counter = 1
    sheet.write(0,0,[unicode("cross_status").encode('utf-8') ])
    for index_i,field in enumerate(field_names):
         sheet.write(0,1+index_i,[unicode(field).encode('utf-8') ])
         index_counter +=1

    for index_i,field in enumerate(cross_status_fields):
         sheet.write(0,index_counter+index_i,[unicode(field).encode('utf-8') ])


    for index_i,an_order in enumerate(orders):

        cross_statuss = OrderCrossDetails.objects.get( order = an_order)
        a_cross_statuss = cross_statuss.cross_status
        for index_j,field in enumerate(order_cross_details_fields):
            sheet.write(index_i+1,index_j,[unicode(getattr(a_cross_statuss, field)).encode('utf-8') ])

        for index_j,field in enumerate(field_names):
            if index_j == 11 or index_j == 10:
                sheet.write(index_i+1,index_j+1,Decimal(getattr(an_order, field)))
            else:
                sheet.write(index_i+1,index_j+1,[unicode(getattr(an_order, field)).encode('utf-8') ])

        for index_j,field in enumerate(cross_status_fields):
            sheet.write(index_i+1,index_j+index_counter,[unicode(getattr(cross_statuss, field)).encode('utf-8') ])

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    if supplier.name == "" and "transaction_keyword" in request.GET:
        file_string = 'attachment; filename='+request.GET['transaction_keyword']+'.xls'
        response['Content-Disposition'] = file_string
    else:
        file_string = 'attachment; filename='+slugify(supplier.name)+'_'+str(end_date)+'_'+str(start_date)+'.xls'
        response['Content-Disposition'] = file_string

    book.save(response)
    return response

@login_required
def exportExcelTransactions(request):
    code= ""
    cs = None

    if "code" in request.GET:
        code = request.GET["code"]
    try:
        cs = CrossStatus.objects.get(pk = int(request.GET['cstatus']))
    except:
        pass

    given_transaction = Transactions.objects.get(code = code)
    orderTransactionPairs = OrderTransaction.objects.filter(trans = given_transaction)
    if cs is not None:
        orderTransactionPairs = orderTransactionPairs.filter(order__ordercrossdetails__cross_status=cs)
    orders = list()
    for aPair in orderTransactionPairs:
        anOrder = Order.objects.get(pk = aPair.order.id)
        orders.append(anOrder)


    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    field_names = ['id_sales_order_item','order_nr','size','sku','sku_supplier_config','sku_supplier_simple','barcode_ean','name','status','suborder_number','paid_price','cost','tax_percent','tax_amount','order_date']
    cross_status_fields = ['order_attribute','inbound_order_number','supplier_order_date',]
    order_cross_details_fields = ['name']

    index_counter = 1
    sheet.write(0,0,[unicode("cross_status").encode('utf-8') ])
    for index_i,field in enumerate(field_names):
         sheet.write(0,1+index_i,[unicode(field).encode('utf-8') ])
         index_counter +=1

    for index_i,field in enumerate(cross_status_fields):
         sheet.write(0,index_counter+index_i,[unicode(field).encode('utf-8') ])


    for index_i,an_order in enumerate(orders):

        cross_statuss = OrderCrossDetails.objects.get( order = an_order)
        a_cross_statuss = cross_statuss.cross_status
        for index_j,field in enumerate(order_cross_details_fields):
            sheet.write(index_i+1,index_j,[unicode(getattr(a_cross_statuss, field)).encode('utf-8') ])

        for index_j,field in enumerate(field_names):
            if index_j == 11 or index_j == 10:
                sheet.write(index_i+1,index_j+1,Decimal(getattr(an_order, field)))
            else:
                sheet.write(index_i+1,index_j+1,[unicode(getattr(an_order, field)).encode('utf-8') ])

        for index_j,field in enumerate(cross_status_fields):
            sheet.write(index_i+1,index_j+index_counter,[unicode(getattr(cross_statuss, field)).encode('utf-8') ])

    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+code+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response

@login_required
def exportExcelForSupplier(request):
    code= ""
    cs = None

    if "code" in request.GET:
        code = request.GET["code"]
    try:
        cs = CrossStatus.objects.get(pk = int(request.GET['cstatus']))
    except:
        pass

    given_transaction = Transactions.objects.get(code = code)
    orderTransactionPairs = OrderTransaction.objects.filter(trans = given_transaction)
    if cs is not None:
        orderTransactionPairs = orderTransactionPairs.filter(order__ordercrossdetails__cross_status=cs)
        
    orders = list()
    skus = dict()
    total_costs = dict()
    total_cost = 0
    for aPair in orderTransactionPairs:
        anOrder = Order.objects.get(pk = aPair.order.id)
        sku = aPair.order.sku
        cost = float(aPair.order.cost)
        total_cost = total_cost + cost
        orders.append(anOrder)
        num_of_same_sku = orderTransactionPairs.filter(order__sku=sku).count()
        skus[sku] = num_of_same_sku
        total_costs[sku]  = cost * float(num_of_same_sku)

    x = 5
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')
    field_names = ['name','sku','sku_supplier_config','sku_supplier_simple','barcode_ean','size','tax_percent','tax_amount','cost']

    index_counter = 1
    sheet.write(0,0,[unicode("Urun Adi").encode('utf-8') ])
    sheet.write(0,1,[unicode("Zidaya SKU").encode('utf-8') ])
    sheet.write(0,2,[unicode("Tedarikci SKU Config").encode('utf-8') ])
    sheet.write(0,3,[unicode("Tedarikci SKU Simple").encode('utf-8') ])
    sheet.write(0,4,[unicode("Barkod").encode('utf-8') ])
    sheet.write(0,5,[unicode("Beden/Boyut").encode('utf-8') ])

    sheet.write(0,6,[unicode("KDV Orani").encode('utf-8') ])
    sheet.write(0,7,[unicode("KDV Tutari").encode('utf-8') ])

    sheet.write(0,8,[unicode("Tutar").encode('utf-8') ])
    sheet.write(0,9,[unicode("Miktar").encode('utf-8') ])
    sheet.write(0,10,[unicode("Toplam Tutar").encode('utf-8') ])

#    sheet.write(0,6,[unicode("Tutar").encode('utf-8') ])
#    sheet.write(0,7,[unicode("Miktar").encode('utf-8') ])
#    sheet.write(0,8,[unicode("Toplam Tutar").encode('utf-8') ])

    count_j = 0
    row_fixer = 0
    
    num_of_item_listed = skus.__len__()
    for index_i,an_order in enumerate(orders):
        if an_order.sku in skus:
            for index_j,field in enumerate(field_names):
                if index_j == 6 or index_j == 7 or index_j == 8:
                    sheet.write(index_i+1-row_fixer,index_j,Decimal(getattr(an_order, field)))
                else:
                    sheet.write(index_i+1-row_fixer,index_j,[unicode(getattr(an_order, field)).encode('utf-8') ])
                count_j = index_j

            sheet.write(index_i+1-row_fixer,count_j+1,skus[an_order.sku])
            sheet.write(index_i+1-row_fixer,count_j+2,total_costs[an_order.sku])
            skus.pop(an_order.sku)
        else:
            row_fixer = row_fixer + 1

    sheet.write(num_of_item_listed+2,9,[unicode('Genel Toplam').encode('utf-8') ])
    sheet.write(num_of_item_listed+2,10,total_cost)
    response = HttpResponse(mimetype='application/vnd.ms-excel')

    file_string = 'attachment; filename='+code+'.xls'
    response['Content-Disposition'] = file_string

    book.save(response)
    return response

