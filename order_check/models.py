from django.db import models
from django.contrib import admin

# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50)
    quantity = models.IntegerField(max_length=10)
    def __unicode__(self):
        return self.order_number

class CrossStatus(models.Model):
    order_status   = models.CharField(max_length=30,default='unprocessed')
    order_id      = models.ForeignKey(Order, primary_key= True)
    def __unicode__(self):
        return str(self.order_id)+' '+self.order_status

class Admin:
   prepopulated_fields = {'slug': ('title',)}
   fieldsets = [
       (None,               {'fields': ['title']}),
       ('Date information', {'fields': ['body'],'classes': ['collapse']})
   ]

admin.site.register(Order)
admin.site.register(CrossStatus)