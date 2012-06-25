from django.db import models
from cross_app.cross_order.models import Supplier
from django.contrib.auth.models import User
from datetime import  datetime
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
import settings

class OrderItemBaseForReturns(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,null=False,default=0)
    id_sales_order = models.PositiveIntegerField(max_length=10,null=True)
    id_catalog_simple = models.IntegerField(max_length=11,null=False)
    order_nr = models.CharField(max_length=45,null=True,primary_key=True)
    sku = models.CharField(max_length=255,null=True)
    order_date = models.DateTimeField(blank=True)
    supplier_name = models.CharField(max_length=511,null=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    suborder_number = models.CharField(max_length=20,null=True)
    paid_price = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    shipping_name = models.CharField(max_length=511,null=True)
    billing_name = models.CharField(max_length=511,null=True)
    billing_name = models.CharField(max_length=511,null=True)
    customer_email = models.CharField(max_length=511,null=True)
    address1 = models.CharField(max_length=255,null=True)
    address2 = models.CharField(max_length=255,null=True)
    billing_address = models.CharField(max_length=255,null=True)
    billing_address2 = models.CharField(max_length=255,null=True)
    payment_method = models.CharField(max_length=511,null=True)
    coupon_code = models.CharField(max_length=511,null=True)
    coupon_money_value = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    coupon_percent = models.IntegerField(max_length=11,null=True)
    bob_status = models.CharField(max_length=255,null=True)
    def __unicode__(self):
        return str(self.order_nr)

    class Meta:
        db_table = 'rts_orderitemview'

class ActionType(models.Model):
    name = models.CharField(max_length=250,null=False)
    isInvalid = models.BooleanField(null=False,default=False)
    order = models.IntegerField(default=9999)

class ReturnReason(models.Model):
    name = models.CharField(max_length=250,null=False)
    isInvalid = models.BooleanField(null=False,default=False)
    order = models.IntegerField(default=9999)

class ReturnedItemDetails(models.Model):
    order_item = models.ForeignKey(OrderItemBaseForReturns,unique=True,null=False)
    return_reason = models.ForeignKey(ReturnReason,unique=False,null=False)
    action_type = models.ForeignKey(ActionType,unique=False,null=False)
    comment = models.TextField(null=True)
    time_stamp = models.DateTimeField(default= datetime.now())

