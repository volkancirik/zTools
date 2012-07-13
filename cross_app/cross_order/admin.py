from django.contrib import admin
from cross_order.models import Supplier, CrossStatus, Order, OrderCrossDetails, LastUpdate, Transactions, OrderTransaction, OrderAttributeSet, TransactionStatus, Sql2ExcelColumn, ReportSql2Excel, InvoiceInfoForTransactions

class Sql2ExcelColumnInline(admin.TabularInline):
    model = Sql2ExcelColumn
    extra = 10

class ReportSql2ExcelAdmin(admin.ModelAdmin):
    inlines = [Sql2ExcelColumnInline]

admin.site.register(ReportSql2Excel,ReportSql2ExcelAdmin)
admin.site.register(Supplier)
admin.site.register(CrossStatus)
admin.site.register(Order)
admin.site.register(OrderCrossDetails)
admin.site.register(LastUpdate)
admin.site.register(Transactions)
admin.site.register(TransactionStatus)
admin.site.register(OrderTransaction)
admin.site.register(OrderAttributeSet)
admin.site.register(InvoiceInfoForTransactions)