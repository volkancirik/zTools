from django.contrib import admin
from cross_order.models import Supplier, CrossStatus, Order, OrderCrossDetails, LastUpdate, Transactions, OrderTransaction, OrderAttributeSet, TransactionStatus

admin.site.register(Supplier)
admin.site.register(CrossStatus)
admin.site.register(Order)
admin.site.register(OrderCrossDetails)
admin.site.register(LastUpdate)
admin.site.register(Transactions)
admin.site.register(TransactionStatus)
admin.site.register(OrderTransaction)
admin.site.register(OrderAttributeSet)