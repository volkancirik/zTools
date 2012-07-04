
#! /usr/bin/env python
import random

import sys
import os
import datetime
from rts.helper import FROM_EMAIL_SUBJECT, FROM_EMAIL_NAME

def setup_environment():

    sys.path.append('C:/Projects/DjangoProjects/zTools')
    sys.path.append('C:/Projects/DjangoProjects/zTools/cross_app')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cross_app.settings'
setup_environment()

def fixSizes():
    from django.core.mail.message import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from rts.models import ReturnedItemDetails, rts_status

    for item in ReturnedItemDetails.objects.filter(status = rts_status.REFUNDED,isEmailSent=False):

        from_email = "<musterihizmetleri@zidaya.com>"
        from_name = str(FROM_EMAIL_NAME)
        #to = item.order_item.customer_email
        to = "baris.bilgic@rocket-internet.com.tr"

        subject = str(FROM_EMAIL_SUBJECT)
        html_content = render_to_string('zidaya_return_email_template_1.html', {
            'billing_name':item.order_item.billing_name.title(),
            'order_date': str(item.order_item.order_date.day).zfill(2)+"."+str(item.order_item.order_date.month).zfill(2)+"."+str(item.order_item.order_date.year),
            'order_nr':item.order_item.order_nr,
            'paid_price':item.order_item.paid_price,
            'refund_reference_number':item.refund_reference_number,
            'product_image':"http://static.zidaya.com/p/-"+str(item.order_item.id_catalog_config)[::-1]+"-1-catalog.jpg",
            'name':item.order_item.name,
            'new_coupon':item.new_coupon,
            'sku':item.order_item.sku
            })
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_name+" "+from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            item.isEmailSent = True
            item.save()
        except:
            pass

		


fixSizes()
