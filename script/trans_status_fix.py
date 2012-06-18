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

    from cross_order.models import Transactions, TransactionStatus

    tList = Transactions.objects.filter(create_date__lte=datetime.datetime.strptime("31/05/2012:23:59:59","%d/%m/%Y:%H:%M:%S"))

    ts = TransactionStatus.objects.filter(order=20)
    for t in tList:
        t.status = ts
        #t.save()
        print t.code


fixSizes()
