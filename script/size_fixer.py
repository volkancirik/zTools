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
    
    print "Sizes are been fetching and updating..."
    
    
    oList = Order.objects.all().filter(size=None)

    print len(oList)

    counter = 0
    for no in oList:
	try:
		no.size = SimpleSize.objects.get(fk_catalog_simple=int(no.sku.split('-')[1])).size
		#print no.size
		print no.sku
		no.save()
	except:
		print "Error " + no.sku
		pass
		

fixSizes()
