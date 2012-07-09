from cross_order.helper_functions import render_response

def home(request):
    err_message = ""
    err_module = request.GET.get("err_module_name",None)
    if err_module is not None:
        if err_module == "cross":
            err_message = "Cross Order Management: "
        elif err_module == "rts":
            err_message = "Returned Item Tracking System: "
        elif err_module == "dms":
            err_message = "Document Management System: "

        err_message += str(_("dont_have_permission_for_module"))

    return render_response(request, 'home.html',{'err_message':err_message})