from django.db import models
from datetime import  datetime

class Shipment(models.Model):
    code = models.CharField(max_length=1000,null=False)
    start_date = models.DateTimeField(default= datetime.now())
    end_date = models.DateTimeField(default= datetime.now())

    def __unicode__(self):
        return self.code


class ShipmentItem(models.Model):
    code = models.IntegerField(default=0)
    shipment = models.ForeignKey(Shipment)
    quantity = models.IntegerField(default=0)
    barcode = models.CharField(max_length=1000,null=False)
    sku = models.CharField(max_length=1000,null=True)
    photo_url = models.CharField(max_length=1000,null=True)
    
    quantity_received = models.IntegerField(default=0)
    quantity_stocked = models.IntegerField(default=0)
    quantity_damaged = models.IntegerField(default=0)
    quantity_photomismatch = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.sku
