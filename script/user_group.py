#! /usr/bin/env python

import sys
import os
import datetime

def setup_environment():

    sys.path.append('/home/opsland/opsland/bin/zTools/')
    sys.path.append('/home/opsland/opsland/bin/zTools/cross_app/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings'
setup_environment()

def fixSizes():

    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group

    grp = Group.objects.get(pk=5)
    for u in User.objects.all():
        grp.user_set.add(u)


fixSizes()
