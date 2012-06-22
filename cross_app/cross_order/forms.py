from django import forms
from cross_order.models import CrossStatus, OrderAttributeSet
from django.utils.translation import gettext_lazy as _

class OrderSearchForm(forms.Form):
    cross_status = forms.ModelChoiceField(label=_("search_cross_status"),queryset = CrossStatus.objects.all(),required=False,empty_label=_("search_all"))
    order_item_id = forms.CharField(required = False,label=_("search_order_item_id"))
    zidaya_order_item = forms.CharField(required = False,label=_("search_zidaya_order_item"))
    sku = forms.CharField(required = False,label=_("search_sku"))

    suborder_number = forms.CharField(required = False,label=_("search_suborder_number"))
    supplier_name = forms.CharField(required = False,label=_("search_supplier_name"))
    attribute_set = forms.ModelChoiceField(label=_("search_attribute_set"),queryset = OrderAttributeSet.objects.all(),required=False,empty_label=_("search_all"))

    supplier_sku_config = forms.CharField(required = False,label=_("search_cross_supplier_sku_config"))
    supplier_sku_simple = forms.CharField(required = False,label=_("search_cross_supplier_sku_simple"))
    barcode = forms.CharField(required = False,label=_("search_cross_barcode"))

    name = forms.CharField(required = False,label=_("search_cross_name"))
    order_date_start = forms.CharField(required = False,label=_("search_cross_order_date_start"))
    order_date_end = forms.CharField(required = False,label=_("search_cross_order_date_end"))

    inbound_order_number = forms.CharField(required = False,label=_("search_inbound_order_number"))
    supplier_order_date_start = forms.CharField(required = False,label=_("search_supplier_order_date_start"))
    supplier_order_date_end = forms.CharField(required = False,label=_("search_supplier_order_date_end"))

    last_update_date_start = forms.CharField(required = False,label=_("search_last_update_date_start"))
    last_update_date_end = forms.CharField(required = False,label=_("search_last_update_date_end"))
    comment = forms.CharField(required = False,label=_("search_comment"))