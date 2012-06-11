import os
import sys

def setup_environment():

    #sys.path.append('/home/opsland/opsland/bin/zTools/')
    #sys.path.append('/home/opsland/opsland/bin/zTools/cross_app/')

    sys.path.append('C:/Projects/DjangoProjects/zTools')
    sys.path.append('C:/Projects/DjangoProjects/zTools/cross_app')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings'
setup_environment()

def removeFiles():
    from dms.models import Document
    from settings import MEDIA_ROOT
    path = MEDIA_ROOT+"uploads/"

    invalid = 0
    for root, dirs, files in os.walk(u'%s'%path):
        for file in files:
                if not Document.objects.filter(file='uploads/'+file).count():
                    if len(file):
                        os.remove(path+file)
                    invalid += 1

    print invalid
    print Document.objects.all().count()

removeFiles()