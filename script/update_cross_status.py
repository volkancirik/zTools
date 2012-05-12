
#! /usr/bin/env python

import sys
import os
import datetime

def setup_environment():

    sys.path.append('/home/opsland/opsland/bin/zTools/')
    sys.path.append('/home/opsland/opsland/bin/zTools/cross_app/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings_cross2'
setup_environment()

def fixSizes():

    from cross_app.cross_order.models import OrderLive,CrossStatus,LastUpdate,Supplier,Order
    from django.contrib.auth.models import User
    from cross_app.cross_order.models import OrderCrossDetails,SimpleSize


    cancelCounter = 0
    shipCounter = 0
    for o in Order.objects.all():
        live = OrderLive.objects.get(id_sales_order_item = o.id_sales_order_item)
        cs = None

	    o.status = live.status
	    o.save()

        # TODO  Remove hardcoded ip by a config. parameter (a boolean field etc.)
        # o.ordercrossdetails.cross_status.pk means SHIPPED
        if live.status == "shipped" and o.ordercrossdetails.cross_status.pk != 7:
            cs = CrossStatus.objects.get(pk=7)
            shipCounter += 1

        if live.status == "canceled" and o.ordercrossdetails.cross_status.pk != 6:
            cs = CrossStatus.objects.get(pk=6)
            cancelCounter += 1


        if cs is not None:
            o.ordercrossdetails.cross_status = cs
            o.ordercrossdetails.save()

            lu = LastUpdate()
            lu.update_date = datetime.datetime.now()
            lu.cross_status = cs
            lu.order = o
            lu.user = User.objects.filter(groups__name="fetcher")[0]
            lu.save()

    print "Total : " + str(Order.objects.all().count())
    print "Shipped : " + str(shipCounter)
    print "Canceled : " + str(cancelCounter)

fixSizes()
