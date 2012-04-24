import sys
import os


def setup_environment():
    sys.path.append('C:/Users/Onur/PycharmProjects')
    sys.path.append('C:/Users/Onur/PycharmProjects/cross_dock_order/')
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_dock_order.settings'

setup_environment()

def fixAttribute():
    from order_check.models import Order
    from order_check.models import CrossStatus
    
    for o in Order.objects.all():
        sku = o.sku
        attribute = sku[5:7]
        o.crossstatus.order_attribute = attribute
        o.crossstatus.save()

fixAttribute()