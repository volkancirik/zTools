from django.contrib import admin
from sms.models import ShipmentType,Shipment,CancellationReason

admin.site.register(ShipmentType)
admin.site.register(Shipment)
admin.site.register(CancellationReason)