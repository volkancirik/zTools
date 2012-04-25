#! /usr/bin/env python

import sys
import os
import datetime

def setup_environment():

    sys.path.append('C:/Users/cirik/Desktop/dropbox/Dropbox/Rocket/projects/')
    sys.path.append('C:/Users/cirik/Desktop/dropbox/Dropbox/Rocket/projects/cross_dock_order/')

    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_dock_order.settings'
setup_environment()

def fixStatus():
    
    from order_check.models import Order
    from order_check.models import CrossStatus
    from order_check.models import LastUpdate
    from order_check.models import UserProfile

    fetcher = UserProfile.objects.get( role = 'F')
    for o in Order.objects.all():

#
#                        anOrder.cross_status = 'Unprocessed'
#                        anOrder.updated_on = datetime.datetime.now()
#                        anOrder.updated_by = fetcher.user.username
        cs = CrossStatus()
        cs.order_id = o
        cs.order_status = "unprocessed"
        cs.save()
        LastUpdate.objects.create(updated_on = datetime.datetime.now() , cross_status = 'unprocessed', order_id = o, user_id = fetcher )

fixStatus()