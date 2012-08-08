import datetime
from django import template
from cross_order.models import Supplier, CrossStatus, OrderTransaction, Transactions, EkolStock
from django.db.models import Sum
register = template.Library()

@register.filter
def todayUnprocessed(sup):
    cs = CrossStatus.objects.all().order_by("order")[0]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max) 
    return sup.order_set.filter(ordercrossdetails__cross_status=cs,order_date__range=(today_min, today_max)).count()

@register.filter
def todayTotal(sup):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    return sup.order_set.filter(order_date__range=(today_min, today_max)).count()

@register.filter
def weekUnprocessed(sup):
    cs = CrossStatus.objects.all().order_by("order")[0]
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    lastweek = today_max - datetime.timedelta(7)
    return sup.order_set.filter(ordercrossdetails__cross_status=cs,order_date__range=(lastweek, today_max)).count()

@register.filter
def weekTotal(sup):
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    lastweek = today_max - datetime.timedelta(7)
    return sup.order_set.filter(order_date__range=(lastweek, today_max)).count()

@register.filter
def totalUnprocessed(sup):
    cs = CrossStatus.objects.all().order_by("order")[0]
    return sup.order_set.filter(ordercrossdetails__cross_status=cs).count()

@register.filter
def total(sup):
    return sup.order_set.all().count()

@register.filter
def totalOrderCount(t):
    return OrderTransaction.objects.filter(trans=t).count()

@register.filter
def totalConfirmed(t):
    cs = CrossStatus.objects.all().order_by("order")[2]
    return OrderTransaction.objects.filter(trans=t,order__ordercrossdetails__cross_status=cs).count()

@register.filter
def totalShipped(t):
    cs = CrossStatus.objects.all().order_by("order")[5]
    return OrderTransaction.objects.filter(trans=t,order__ordercrossdetails__cross_status=cs).count()

@register.filter
def totalCancelled(t):
    cs = CrossStatus.objects.all().order_by("order")[4]
    return OrderTransaction.objects.filter(trans=t,order__ordercrossdetails__cross_status=cs).count()

@register.filter
def getSupplierName(t):
    try:
        return OrderTransaction.objects.filter(trans=t)[0].order.supplier.name
    except:
        return "ERROR - Invalid sup. name"

@register.filter
def getTotalCost(t):
    return OrderTransaction.objects.filter(trans=t).aggregate(Sum('order__cost'))["order__cost__sum"]

@register.filter
def getUser(t):
    return t.create_user.email

@register.filter
def is_dms_user(user):
    if user:
        return user.groups.filter(name='Dms').count() > 0
    return False

@register.filter
def is_rts_warehouse_user(user):
    if user:
        return user.groups.filter(name='RtsWarehouse').count() > 0
    return False

@register.filter
def is_rts_customer_user(user):
    if user:
        return user.groups.filter(name='RtsCustomer').count() > 0
    return False

@register.filter
def None2Empty(value):
    if value is None:
        return ""
    else:
        return value

@register.filter
def reverse(value):
    return str(value)[::-1]

@register.filter
def checkPermission(user, arg=u's'):
    for group_name in arg.split(','):
        return user.groups.filter(name=group_name).count() > 0
    return False

@register.filter
def getSmsQuickAddErrorMessage(type):
    if type == 1:
        return "SKU bulunamadi"
    elif type == 2:
        return "SKU belirtilen Supplier'a ait degil"
    elif type == 3:
        return "Status simple is not active"
    elif type == 4:
        return "Status config is not active"
    elif type == 5:
        return "Shipment type is not ON_WAREHOUSE"
    elif type == 6:
        return "Girilen quantity gecerli degil"
    elif type == 7:
        return "Brand is no active"

@register.filter
def getEkolStock(sku):
    if EkolStock.objects.filter(sku=sku).count():
        return EkolStock.objects.get(sku=sku).available_quantity
    return "0"

@register.filter
def getEkolStockOutPlanned(sku):
    if EkolStock.objects.filter(sku=sku).count():
        return EkolStock.objects.get(sku=sku).stock_out_planned
    return "0"
