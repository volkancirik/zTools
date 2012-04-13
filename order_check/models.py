from django.db import models
from django.contrib import admin
from django.contrib.auth.models import UserManager
from django.core import validators
from django.forms import Form
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('B', 'Buyer'),
        ('O', 'Operations'),
        ('A', 'Admin'),
        ('F','Fetcher')
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        up = instance.get_profile()
        up.save()


post_save.connect(create_user_profile, sender=User)




class Order(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,null=False,default=0)
    id_sales_order = models.PositiveIntegerField(max_length=10,null=True)
    order_nr = models.CharField(max_length=45,null=True)
    size = models.IntegerField(max_length=11,null=True)
    sku = models.CharField(max_length=255,null=True)
    supplier_name = models.CharField(max_length=255,null=True)
    sku_supplier_simple = models.CharField(max_length=50,null=True)
    shipment_type = models.CharField(max_length=255,null=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    sku_supplier_config = models.CharField(max_length=50,null=True)
    buysheet_id = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=255,null=True)
    id_sales_order_item_shipment = models.PositiveIntegerField(max_length=10,null=True)
    tracking_url = models.CharField(max_length=255,null=True)
    suborder_number = models.CharField(max_length=20,null=True)
    paid_price = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    cost = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    shipping_name = models.CharField(max_length=511,null=True)
    shipping_city = models.CharField(max_length=255,null=True)
    billing_name = models.CharField(max_length=511,null=True)
    billing_city = models.CharField(max_length=255,null=True)
    customer_first_name = models.CharField(max_length=255,null=True)
    customer_last_name = models.CharField(max_length=255,null=True)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2, null=False,default=0)
    tax_percent = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    original_unit_price = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    unit_price = models.DecimalField(max_digits=10,decimal_places=2, null=False)
    tax_amount = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    phone = models.CharField(max_length=255,null=True)
    coupon_money_value = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    coupon_percent = models.IntegerField(max_length=11,null=True)
    address1 = models.CharField(max_length=255,null=True)
    address2 = models.CharField(max_length=255,null=True)
    billing_address = models.CharField(max_length=255,null=True)
    billing_address2 = models.CharField(max_length=255,null=True)
    order_date = models.DateTimeField(blank=True, auto_now_add=True)
    def __unicode__(self):
        return str(self.id_sales_order_item)

class CrossStatus(models.Model):
    order_status   = models.CharField(max_length=30,default='unprocessed')
    order_id      = models.OneToOneField(Order,null=False)
    def __unicode__(self):
        return str(self.order_id)+' '+self.order_status

class LastUpdate(models.Model):
    updated_on = models.DateTimeField(blank=False, auto_now_add=True)
    cross_status = models.CharField(max_length=30,default='unprocessed')
    order_id = models.ForeignKey(Order)
    user_id = models.ForeignKey(UserProfile)

    class Meta:
        ordering = ['-updated_on']

    def __unicode__(self):
       return str(self.order_id)+' changed to '+self.cross_status+' on '+str(self.updated_on)+' by '+self.user_id.user.username


class Admin:
   prepopulated_fields = {'slug': ('title',)}
   fieldsets = [
       (None,               {'fields': ['title']}),
       ('Date information', {'fields': ['body'],'classes': ['collapse']})
   ]

#admin.site.register(UserProfile)
#admin.site.register(Order)
#admin.site.register(CrossStatus)
#admin.site.register(LastUpdate)
