from cross_order.helper_functions import render_response
from django.utils.translation import gettext_lazy as _

def home(request):
    err_message = ""
    err_module = request.GET.get("err_module",None)
    if err_module is not None:
        if err_module == "Cross":
            err_message = "Cross Order Management: "
        elif err_module == "RtsWarehouse" or err_module == "RtsCustomer" :
            err_message = "Returned Item Tracking System: "
        elif err_module == "dms":
            err_message = "Document Management System: "

        err_message += str(_("dont_have_permission_for_module"))

    return render_response(request, 'home.html',{'err_message':err_message})