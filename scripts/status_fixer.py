#! /usr/bin/env python

import sys
import os


def setup_environment():
    sys.path.append('C:/Projects/DjangoProjects/')
    sys.path.append('C:/Projects/DjangoProjects/cross_dock_order/')
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_dock_order.settings'
setup_environment()

def fixStatus():
    from order_check.models import Order
    from order_check.models import CrossStatus
    
    for o in Order.objects.all():
        cs = CrossStatus()
        cs.order_id = o
        cs.order_status = "Unprocessed"
        cs.save()


fixStatus()