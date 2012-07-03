
#! /usr/bin/env python
import random

import sys
import os
import datetime

def setup_environment():

    sys.path.append('/home/opsland/opsland/bin/')
    sys.path.append('/home/opsland/opsland/bin/cross_dock_order/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings'
setup_environment()

def fixSizes():

    from main.models import OrderItemBase
    from main.models import Supplier
    from cross_order.models import OrderCrossDetails, CrossOrderItem
    from cross_order.models import LastUpdate, OrderTransaction
    
    for o in OrderCrossDetails.objects.all():
        oib = OrderItemBase.objects.get(id_sales_order_item=o.order.id_sales_order_item)
        coi = CrossOrderItem()
        coi.orderitem = oib
        coi.order_attribute =  o.order_attribute
        coi.cross_status = o.cross_status
        coi.supplier_order_date = o.supplier_order_date
        coi.comment = o.comment
        coi.inbound_order_number = o.inbound_order_number
        coi.save()

        for lu in o.order.lastupdateold_set.all():
            item = LastUpdate()
            item.update_date = lu.update_date
            item.cross_status = lu.cross_status
            item.order = OrderItemBase.objects.get(id_sales_order_item=lu.order.id_sales_order_item)
            item.user = lu.user
            item.save()

        for ot in o.order.ordertransactionold_set.all():
            item = OrderTransaction()
            item.trans = ot.trans
            item.order = OrderItemBase.objects.get(id_sales_order_item=ot.order.id_sales_order_item)
            item.save()


		


fixSizes()
