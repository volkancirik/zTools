from django import forms
from rts.models import OrderItemBaseForReturns, ReturnedItemDetails,ReturnReason,ActionType
from django.utils.translation import gettext_lazy as _

class ReturnedItemForm(forms.Form):
#    cross_status = forms.ModelChoiceField(label=_("search_cross_status"),queryset = CrossStatus.objects.all(),required=False,empty_label=_("search_all"))
#    order_item_id = forms.CharField(required = False,label=_("search_order_item_id"))
#    zidaya_order_item = forms.CharField(required = False,label=_("search_zidaya_order_item"))
    sku = forms.CharField(required = False,label=_("search_sku"))