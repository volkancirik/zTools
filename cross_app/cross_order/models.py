from django.db import models
from django.contrib.auth.models import User
from datetime import  datetime
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

class ColumnType():
    CHAR = 0
    INT = 1
    FLOAT = 2
    
    TYPE = (
            (CHAR,_("CHAR")),
            (INT ,_("INT")),
            (FLOAT ,_("FLOAT")),
            )

class ReportSql2Excel(models.Model):
    name = models.CharField(max_length=2000,null=True)
    excel_name = models.CharField(max_length=2000,null=True)
    tb_name = models.CharField(max_length=2000,null=True)

    isActive = models.BooleanField(null=False,default=True)
    order = models.IntegerField(default=9999)

    def __unicode__(self):
        return str(self.name)

class Sql2ExcelColumn(models.Model):
    report = models.ForeignKey(ReportSql2Excel,unique=False,null=False)
    name = models.CharField(max_length=2000,null=True)
    type = models.IntegerField(default=ColumnType.CHAR,choices=ColumnType.TYPE)

    def __unicode__(self):
        return str(self.name)

class ReportUnprocessedCrossDock(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,primary_key=True)
    suborder_number = models.CharField(max_length=20,null=True)
    order_nr = models.CharField(max_length=45,null=True)
    order_date = models.DateTimeField(blank=True)
    sku = models.CharField(max_length=255,null=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=2000,null=False)
    attribute_set = models.CharField(max_length=50,null=False)
    bob_status = models.CharField(max_length=200,null=True)
    supplier_name = models.CharField(max_length=2000,null=False)

    def __unicode__(self):
        return str(self.sku)

    class Meta:
        db_table = 'unprocessed_crossdock_order_items'

class OverdueCrossDock(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,primary_key=True)
    suborder_number = models.CharField(max_length=20,null=True)
    order_nr = models.CharField(max_length=45,null=True)
    order_date = models.DateTimeField(blank=True)
    sku = models.CharField(max_length=255,null=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=2000,null=False)
    attribute_set = models.CharField(max_length=50,null=False)
    bob_status = models.CharField(max_length=200,null=True)
    days_overdue = models.PositiveIntegerField(max_length=10)
    delivery_time_max = models.PositiveIntegerField(max_length=10)

    def __unicode__(self):
        return str(self.sku)

    class Meta:
        db_table = 'overdue_crossdock_order_items'

class ReportOutOfStockCrossDock(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,primary_key=True)
    suborder_number = models.CharField(max_length=20,null=True)
    order_nr = models.CharField(max_length=45,null=True)
    order_date = models.DateTimeField(blank=True)
    sku = models.CharField(max_length=255,null=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=2000,null=False)
    attribute_set = models.CharField(max_length=50,null=False)
    bob_status = models.CharField(max_length=200,null=True)
    
    def __unicode__(self):
        return str(self.sku)

    class Meta:
        db_table = 'outofstock_crossdock_order_items'

class ReportConfirmedSupplierBase(models.Model):
    item_count = models.IntegerField()
    supplier_name = models.CharField(max_length=2000,null=False)

    def __unicode__(self):
        return str(self.supplier_name)

    class Meta:
        db_table = 'confirmed_number_of_items_supplier_base'

class ReportConfirmedSkuBase(models.Model):
    sku = models.CharField(max_length=255,null=True,primary_key=True)
    barcode_ean = models.CharField(max_length=255,null=True)
    item_count = models.IntegerField()
    name = models.CharField(max_length=2000,null=False)
    attribute_set = models.CharField(max_length=50,null=False)
    supplier_name = models.CharField(max_length=2000,null=False)

    def __unicode__(self):
        return str(self.sku)

    class Meta:
        db_table = 'confirmed_number_of_items_sku_base'
    

class Supplier(models.Model):
    name = models.CharField(max_length=1000,null=False)
    code  = models.CharField(max_length=100,null=False)
    

class CrossStatus(models.Model):
    name = models.CharField(max_length=250,null=False)
    isTransactionGenerate = models.BooleanField(null=False,default=False)
    isFinal = models.BooleanField(null=False,default=False)
    isInvalid = models.BooleanField(null=False,default=False)
    order = models.IntegerField(default=9999)

    def __unicode__(self):
        return str(self.name)

class TransactionStatus(models.Model):
    name = models.CharField(max_length=250,null=False)
    order = models.IntegerField(default=9999)
    def __unicode__(self):
        return self.name

class OrderAttributeSet(models.Model):
    attributeName = models.CharField(max_length=50,null=False)
    attributeCode = models.CharField(max_length=50,null=False)
    isInvalid = models.BooleanField(null=False,default=False)
    createTime = models.DateTimeField(default= datetime.now())
    order = models.IntegerField(default=9999)
    def __unicode__(self):
        return str(self.attributeName)


class Order(models.Model):
    id_sales_order_item = models.PositiveIntegerField(max_length=10,null=False,default=0)
    id_sales_order = models.PositiveIntegerField(max_length=10,null=True)
    order_nr = models.CharField(max_length=45,null=True)
    size = models.CharField(max_length=45,null=True)
    sku = models.CharField(max_length=255,null=True)
    supplier = models.ForeignKey(Supplier,unique=False,null=False)
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
    order_date = models.DateTimeField(blank=True)
    last_status_change = models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return str(self.id_sales_order_item)

class OrderCrossDetails(models.Model):
    order = models.OneToOneField(Order,null=False)
    cross_status   = models.ForeignKey(CrossStatus,unique=False,null=False)

    supplier_order_date = models.DateTimeField(null=True,blank=True)
    order_attribute = models.CharField(max_length=10,null=False)
    inbound_order_number = models.CharField(max_length=30,null=True)
    comment = models.TextField(null=True)
    
    def __unicode__(self):
        return str(self.order)+' '+self.cross_status.name

class LastUpdate(models.Model):
    update_date = models.DateTimeField(blank=False)
    cross_status = models.ForeignKey(CrossStatus,unique=False,null=False)
    order = models.ForeignKey(Order)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-update_date']

    def __unicode__(self):
       return str(self.order_id)+' changed to '+self.cross_status+' on '+str(self.update_date)+' by '+self.user.username

class Transactions(models.Model):
    code = models.CharField(max_length=255,null=True)
    create_date = models.DateTimeField(blank=False)
    create_user = models.ForeignKey(User)
    status   = models.ForeignKey(TransactionStatus,unique=False,null=False)

class OrderTransaction(models.Model):
    trans = models.ForeignKey(Transactions)
    order = models.ForeignKey(Order)

class OrderLive(models.Model):
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
    last_status_change = models.DateTimeField(blank=True)

    def __unicode__(self):
        return str(self.id_sales_order_item)
    
    class Meta:
        db_table = 'orderitem_base'

class SimpleSize(models.Model): 
    fk_catalog_simple = models.PositiveIntegerField(max_length=10,primary_key=True)
    size = models.CharField(max_length=45,null=True)

    class Meta:
        db_table = 'simples_sizes'
