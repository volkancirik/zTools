import datetime
import random
from string import split
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
import xlwt

def modelToExcel(data,field_names,file_name):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    index_counter = 1
    for index_i,field in enumerate(field_names):
         sheet.write(0,1+index_i,[unicode(field).encode('utf-8') ])
         index_counter +=1

    for index_i,an_order in enumerate(data):
        for index_j,field in enumerate(field_names):
            sheet.write(index_i+1,index_j+1,[unicode(getattr(an_order, field)).encode('utf-8') ])

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