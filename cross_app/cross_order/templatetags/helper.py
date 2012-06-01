import datetime
from django import template
from cross_order.models import Supplier, CrossStatus, OrderTransaction, Transactions
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
def getSupplierName(t):
    return OrderTransaction.objects.filter(trans=t)[0].order.supplier.name

@register.filter
def getTotalCost(t):
    return OrderTransaction.objects.filter(trans=t).aggregate(Sum('order__cost'))["order__cost__sum"]

@register.filter
def getUser(t):
    return t.create_user.email