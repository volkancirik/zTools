from django.contrib import admin
from rts.models import OrderItemBaseForReturns,ActionType,ReturnedItemDetails,ReturnReason

admin.site.register(OrderItemBaseForReturns)
admin.site.register(ActionType)
admin.site.register(ReturnedItemDetails)
admin.site.register(ReturnReason)