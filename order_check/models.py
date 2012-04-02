from django.db import models
from django.contrib import admin

# Create your models here.
class Order(models.Model):
    id_sales_order_item = models.IntegerField(max_length=10)
    order_nr = models.CharField(max_length=50)
    size = models.IntegerField(max_length=11)
    sku = models.CharField(max_length=255)
    supplier_name = models.CharField(max_length=255)
    sku_supplier_simple = models.CharField(max_length=50)
    shipment_type = models.CharField(max_length=255)
    buysheet_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    paid_price = models.DecimalField(max_digits=10,decimal_places=2)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    def __unicode__(self):
        return self.order_nr

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