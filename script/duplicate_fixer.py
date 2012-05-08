
#! /usr/bin/env python

import sys
import os
import datetime

def setup_environment():

    sys.path.append('/home/opsland/opsland/bin/zerd/')
    sys.path.append('/home/opsland/opsland/bin/zerd/zerd_app/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'zerd_app.settings_cross2'
setup_environment()

def fixSizes():

    from cross_app.cross_order.models import OrderLive,CrossStatus,LastUpdate,Supplier,Order
    from django.contrib.auth.models import User
    from cross_app.cross_order.models import OrderCrossDetails,SimpleSize
    
      
    oList = Order.objects.filter(order_date__range=[datetime.datetime.strptime("30/04/2012:18:00:00","%d/%m/%Y:%H:%M:%S"),datetime.datetime.strptime("04/05/2012:14:00:00","%d/%m/%Y:%H:%M:%S")])

    print len(oList)
    
    count = 0
    for o in OrderLive.objects.using('baytas').filter(order_date__range=[datetime.datetime.strptime("30/04/2012:18:00:00","%d/%m/%Y:%H:%M:%S"),datetime.datetime.strptime("04/05/2012:14:00:00","%d/%m/%Y:%H:%M:%S")]):

	if o.status == "canceled" or o.status == "invalid":
		continue

	if not o.shipment_type.lower().__contains__("crossdocking"):
		continue

	count += 1


    print count

    dupList = []
    counter = 0
    for no in oList:
	if Order.objects.filter(id_sales_order_item = no.id_sales_order_item).count() > 1:
		if no.id_sales_order_item not in dupList:
			dupList.append(no.id_sales_order_item)


    for it in dupList:
	print it

		


fixSizes()
