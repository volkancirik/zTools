#! /usr/bin/env python

import sys
import os
import datetime

def setup_environment():

    sys.path.append('/home/opsland/opsland/bin/')
    sys.path.append('/home/opsland/opsland/bin/cross_dock_order/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_dock_order.settings_cross'
setup_environment()

def fixStatus():

    from order_check.models import Order
    from order_check.models import CrossStatus
    from order_check.models import LastUpdate
    from order_check.models import UserProfile
    from order_check.models import OrderLive
    import datetime

#    startdate = datetime.datetime.strptime("26/04/2012:15:00:00","%d/%m/%Y:%H:%M:%S")
#    enddate = startdate + datetime.timedelta(hours=2)
    t = Order.objects.all().order_by('-order_date')[:1][0]
    
	
    fetcher = UserProfile.objects.get( role = 'F')
    orderList = OrderLive.objects.using('baytas').filter(order_date__range=[t.order_date,datetime.datetime.now()])
    for o in orderList:
        if o.status == "invalid" or o.status == "canceled":
            continue

        no = Order()
        no.id_sales_order_item = o.id_sales_order_item
        no.id_sales_order = o.id_sales_order
        no.order_nr = o.order_nr
        no.size = o.size
        no.sku = o.sku
        no.supplier_name = o.supplier_name
        no.sku_supplier_simple = o.sku_supplier_simple
        no.shipment_type = o.shipment_type
        no.barcode_ean = o.barcode_ean
        no.sku_supplier_config = o.sku_supplier_config
        no.buysheet_id = o.buysheet_id
        no.name = o.name
        no.status = o.status
        no.id_sales_order_item_shipment = o.id_sales_order_item_shipment
        no.tracking_url = o.tracking_url
        no.suborder_number = o.suborder_number
        no.paid_price = o.paid_price
        no.cost = o.cost
        no.shipping_name = o.shipping_name
        no.shipping_city = o.shipping_city
        no.billing_name = o.billing_name
        no.billing_city = o.billing_city
        no.customer_first_name = o.customer_first_name
        no.customer_last_name = o.customer_last_name
        no.amount_paid = o.amount_paid
        no.tax_percent = o.tax_percent
        no.original_unit_price = o.original_unit_price
        no.unit_price = o.unit_price
        no.tax_amount = o.tax_amount
        no.phone = o.phone
        no.coupon_money_value = o.coupon_money_value
        no.coupon_percent = o.coupon_percent
        no.address1 = o.address1
        no.address2 = o.address2
        no.billing_address = o.billing_address
        no.billing_address2 = o.billing_address2
        no.order_date = o.order_date

        no.save()
        cs = CrossStatus()
        cs.order_id = no
        cs.order_attribute = no.sku[5:7]
        cs.save()
        LastUpdate.objects.create(updated_on = datetime.datetime.now() , cross_status = 'unprocessed', order_id = no, user_id = fetcher )

fixStatus()
