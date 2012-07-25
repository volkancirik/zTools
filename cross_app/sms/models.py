from django.db import models
from cross_app.cross_order.models import Supplier
from django.contrib.auth.models import User
from datetime import  datetime
from django.utils.translation import gettext_lazy as _
import settings

class ShipmentStatus():
    REQUESTED  = 0
    CONFIRMED  = 1
    DENIED_BY_OPS  = 2
    DENIED_BY_WH   = 3
    RECEIVED   = 4

    TYPE = (
            (REQUESTED,_("shipment_status_requested")),
            (CONFIRMED,_("shipment_status_confirmed")),
            (DENIED_BY_OPS,_("shipment_status_denied_by_ops")),
            (DENIED_BY_WH,_("shipment_status_denied_by_wh")),
            (RECEIVED,_("shipment_status_recieved")),
            )
class SimpleStatus():
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class BrandStatus():
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class SupplierStatus():
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class SimpleShipmentTypeID():
    ON_WAREHOUSE = 1
    CROSS_DOCKING = 3
    CROSS_DOCKING_JW = 4

class CatalogSupplier(models.Model):
    id_catalog_supplier = models.PositiveIntegerField(max_length=10,unique=True,primary_key=True)
    name = models.CharField(max_length=1000,null=False)
    status = models.CharField(max_length=50,null=True)
    name_en = models.CharField(max_length=1000,null=True)
    order_email  = models.CharField(max_length=1000,null=True)
    contact_email = models.CharField(max_length=1000,null=True)
    contact = models.CharField(max_length=1000,null=True)
    phone = models.CharField(max_length=1000,null=True)
    customercare_phone = models.CharField(max_length=1000,null=True)
    ops_person = models.CharField(max_length=1000,null=True)
    ops_phone = models.CharField(max_length=1000,null=True)
    ops_email = models.CharField(max_length=1000,null=True)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        db_table = 'catalog_supplier'


class CatalogBrand(models.Model):
    id_catalog_brand = models.PositiveIntegerField(max_length=10,unique=True,primary_key=True)
    name = models.CharField(max_length=1000,null=False)
    status = models.CharField(max_length=50,null=True)
    name_en = models.CharField(max_length=1000,null=True)
    url_key = models.CharField(max_length=1000,null=True)
    image_name = models.CharField(max_length=1000,null=True)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        db_table = 'catalog_brand'
    
class CatalogSimple(models.Model):
    id_catalog_simple = models.PositiveIntegerField(max_length=10,unique=True,primary_key=True)
    id_catalog_config = models.PositiveIntegerField(max_length=10)
    sku = models.CharField(max_length=255,null=True)
    sku_config = models.CharField(max_length=255,null=True)
    status_simple = models.CharField(max_length=255,null=True)
    status_config = models.CharField(max_length=255,null=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    tax_percent = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    is_consignment = models.BooleanField(null=False,default=False)
    barcode_ean = models.CharField(max_length=255,null=True)
    id_barcode_to_export = models.PositiveIntegerField(max_length=10,default=0)
    barcode_to_export = models.CharField(max_length=255,null=True)
    barcodes_additional = models.CharField(max_length=255,null=True)
    supplier = models.ForeignKey(CatalogSupplier,unique=False,null=False)
    brand = models.ForeignKey(CatalogBrand,unique=False,null=False)
    sku_supplier_config = models.CharField(max_length=50,null=True)
    sku_supplier_simple = models.CharField(max_length=50,null=True)
    shipment_type = models.CharField(max_length=255,null=True)
    id_shipment_type = models.PositiveIntegerField(max_length=10)
    zidaya_name = models.CharField(max_length=1000,null=True)
    supplier_color = models.CharField(max_length=255,null=True)
    supplier_material = models.CharField(max_length=255,null=True)
    supplier_product_name = models.CharField(max_length=255,null=True)

    def __unicode__(self):
        return str(self.sku)

    class Meta:
        db_table = 'sms_catalog_simple'

class ShipmentType(models.Model):
    name = models.CharField(max_length=250,null=False)
    order = models.IntegerField(default=9999)
    def __unicode__(self):
        return self.name

class CancellationReason(models.Model):
    name = models.CharField(max_length=250,null=False)
    isInvalid = models.BooleanField(null=False,default=False)
    order = models.IntegerField(default=9999)
    def __unicode__(self):
        return self.name

class Shipment(models.Model):
    number = models.CharField(max_length=1000,null=False)
    supplier = models.ForeignKey(CatalogSupplier,unique=False,null=False)

    cancel_reason = models.ForeignKey(CancellationReason)

    is_consignment = models.BooleanField(null=False,default=False)
    create_date = models.DateTimeField(default= datetime.now())
    create_user = models.ForeignKey(User, related_name='%(class)s_user_create')
    update_date = models.DateTimeField(default= datetime.now())
    update_user = models.ForeignKey(User, related_name='%(class)s_user_update')

    shipmentType = models.ForeignKey(ShipmentType,unique=False,null=False)
    status = models.IntegerField(default=ShipmentStatus.REQUESTED,choices=ShipmentStatus.TYPE)
    proposed_shipment_date = models.DateTimeField(default= datetime.now())
    confirmed_shipment_date = models.DateTimeField(null=True)
    date_received = models.DateTimeField(null=True)
    totalShipmentItemCount = models.IntegerField(default=0)
    items = models.ManyToManyField(CatalogSimple,through="ShipmentItem",related_name='items')

    comment = models.TextField(null=True)
    def __unicode__(self):
        return self.number

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment)
    catalog_simple = models.ForeignKey(CatalogSimple)
    quantity_ordered = models.IntegerField(default=0)
    quantity_received = models.IntegerField(default=0)
    quantity_stocked = models.IntegerField(default=0)
    quantity_damaged = models.IntegerField(default=0)
    quantity_photomismatch = models.IntegerField(default=0)

    def __unicode__(self):
        return self.catalog_simple.sku
