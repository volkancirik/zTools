from django.utils.translation import gettext_lazy as _

def not_in_rts_warehouse_group(user):
    if user and user.groups.filter(name='RtsWarehouse').count() > 0:
        return True
    return False

def not_in_rts_customer_group(user):
    if user and user.groups.filter(name='RtsCustomer').count() > 0:
        return True
    return False

FROM_EMAIL_NAME = _("rts_email_from_name")
FROM_EMAIL_SUBJECT = _("rts_email_subject")