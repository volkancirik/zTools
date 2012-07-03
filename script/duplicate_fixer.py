
#! /usr/bin/env python
import random

import sys
import os
import datetime

def setup_environment():

    sys.path.append('C:/Projects/DjangoProjects/zTools')
    sys.path.append('C:/Projects/DjangoProjects/zTools/cross_app')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings'
setup_environment()

def fixSizes():

    from main.models import OrderItemBase
    from main.models import Supplier
    
      
    for o in OrderItemBase.objects.all():
        o.supplier = random.choice(Supplier.objects.all())
        o.save()

		


fixSizes()
