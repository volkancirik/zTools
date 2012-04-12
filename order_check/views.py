# Create your views here.


from models import Order
from models import CrossStatus
from models import UserProfile
from models import LastUpdate
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from datetime import date
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404, HttpResponse
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

def main(request):
    return render_to_response('main.html', context_instance = RequestContext(request))

class SupplierDetails:
    item_count = 0
    supplier_name = ""


@login_required
def order(request):
    supNameDetail = ""
    end_date=""
    start_date=""
    counter = 0
    if "dateEnd" in request.POST:
        end_date = datetime.datetime.strptime(request.POST['dateEnd'], "%m/%d/%Y")
    if "dateStart" in request.POST:
        start_date = datetime.datetime.strptime(request.POST['dateStart'], "%m/%d/%Y")

    if "supname" in request.GET:
       supNameDetail = request.GET["supname"]
    try:
        if start_date != "" and end_date != "":
            ordersAll = Order.objects.filter(order_date__range =[start_date,end_date] )
        else:
            ordersAll = Order.objects.all()
            
        suppliers = list()
        for anOrder in ordersAll:
            if not suppliers.__contains__(anOrder.supplier_name):
                suppliers.append(anOrder.supplier_name)
#                    try:
#                        statusForAnOrder = CrossStatus.objects.get( pk = anOrder.id)
#                        anOrder.cross_status = statusForAnOrder.order_status
#                        latest_update = LastUpdate.objects.filter( order_id = anOrder.id).order_by('-updated_on')
#                        anOrder.updated_on = latest_update[0].updated_on
#                        anOrder.updated_by = latest_update[0].user_id.user.username
#
#                    except CrossStatus.DoesNotExist:
#                        statusForAnOrder = CrossStatus.objects.create(order_id = anOrder,order_status = 'Unprocessed')
#                        fetcher = UserProfile.objects.get( role = 'F')
#                        LastUpdate.objects.create(updated_on = datetime.datetime.now() , cross_status = 'Unprocessed', order_id = anOrder, user_id = fetcher )
#                        anOrder.cross_status = 'Unprocessed'
#                        anOrder.updated_on = datetime.datetime.now()
#                        anOrder.updated_by = fetcher.user.username

        supplierIndex = 0
        supplierDetailList = []
        for aSupplier in suppliers:
            if start_date !="" and end_date != "":
                ic = Order.objects.filter(supplier_name=suppliers.__getitem__(supplierIndex),order_date__range =[start_date,end_date]).count()
            else:
                ic = Order.objects.filter(supplier_name=suppliers.__getitem__(supplierIndex)).count()

            sd = SupplierDetails()
            sd.item_count = ic
            sd.supplier_name = suppliers.__getitem__(supplierIndex)
            supplierDetailList.append(sd)
            supplierIndex = supplierIndex + 1

        if supNameDetail == "":
            supNameDetail = "All Suppliers"
            
        return render_to_response('orders.html', {'supplierDetailList' : supplierDetailList,'supNameDetail':supNameDetail,'end_date':end_date,'start_date':start_date,'counter':counter},context_instance = RequestContext(request))
    except Order.DoesNotExist:
        raise Http404


def listOrders(request):

    supNameDetail=""
    startDate = ""
    endDate = ""

    if "supname" in request.GET:
        supNameDetail = request.GET["supname"]

#    if "startdate" in request.GET:
#        startDate = request.GET["startdate"]
#
#    if "enddate" in request.GET:
#        endDate = request.GET["enddate"]

    if "dateEnd" in request.POST:
        end_date = datetime.datetime.strptime(request.POST['startdate'], "%d/%M/%Y")
    if "dateStart" in request.POST:
        start_date = datetime.datetime.strptime(request.POST['enddate'], "%d/%M/%Y")

    if supNameDetail == "":
        filteredOrders = Order.objects.all()
    else:
        filteredOrders = Order.objects.filter(supplier_name=supNameDetail,order_date__range =[start_date,end_date])

    if request.GET.has_key('page'):
        page = request.GET['page']
    else:
        page = 1

    paginator = Paginator(filteredOrders, 10)
    try:
        orders = paginator.page(page)
    except (EmptyPage, InvalidPage):
        orders = paginator.page(paginator.num_pages)

    return render_to_response('orderList.html',
            {'orders' : orders,
             'supNameDetail':supNameDetail,
             'endDate':endDate,
             'startDate':startDate},context_instance = RequestContext(request))

@login_required
def updateOrder(request):

    orderIDs = list()
    orderIDs = request.POST.getlist('orderChecked')

    for anOrderID in orderIDs:
        try:
            anOrder = Order.objects.get(pk = int(anOrderID))
        except Order.DoesNotExist:
            raise Http404
        try:
            toBeUpdated = CrossStatus.objects.get(pk = anOrder.id)
        except CrossStatus.DoesNotExist:
            toBeUpdated = CrossStatus.objects.create(order_id = anOrder)
        toBeUpdated.order_status =  request.POST["status"]
        toBeUpdated.save()
        active_user = UserProfile.objects.get(user = request.user)
        LastUpdate.objects.create(updated_on = datetime.datetime.now() , cross_status = toBeUpdated.order_status, order_id = anOrder, user_id =  active_user )
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def sort(request,criteria):

    if criteria == "order_id":
        orders = Order.objects.order_by('-order_nr')
    for anOrder in orders:
        try:
            statusForAnOrder = CrossStatus.objects.get( pk = anOrder.id)
            anOrder.status = statusForAnOrder.order_status
        except CrossStatus.DoesNotExist:
            statusForAnOrder = CrossStatus.objects.create(order_id = anOrder,order_status = 'Unprocessed')
            anOrder.status = 'Unprocessed'
    return render_to_response('orders.html', {'orders' : orders},context_instance = RequestContext(request) )

def test(request):
    return render_to_response('asd.html',context_instance = RequestContext(request) )

def tabletest(request):
    return render_to_response('tableTest.html',context_instance = RequestContext(request) )

def registerUser(request):
    if request.POST:
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            User.objects.get(username = email.split('@')[0])
        except User.DoesNotExist:
            user = User.objects.create_user(email.split('@')[0], email, password)
            user.first_name = firstName
            user.last_name = lastName
        else:
            return render_to_response('main.html')

        #profile = user.get_profile()
        #profile.role = 2

        user.save()
        login(request, user)
        return HttpResponseRedirect("/orders/")
    
    else:
        return HttpResponseRedirect("/orders/")

def loginUser(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email.split('@')[0], password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/orders/")
            else:
                print "Your account has been disabled!"
        else:
            print "Your username and password were incorrect."


    else:
            return HttpResponseRedirect("/orders/")

def orderHistory(request,order_id):

    
    update_list = LastUpdate.objects.filter( order_id = order_id).order_by('updated_on')

    user_list = list()
    date_list = list()
    status_list = list()

    for anUpdate in update_list:
        date_list.append(str(anUpdate.updated_on))
        user_list.append(str(anUpdate.user_id.user.username))
        status_list.append(str(anUpdate.cross_status))

    return HttpResponse(simplejson.dumps({'users': user_list, 'dates' : date_list,'statuses' : status_list}),mimetype='application/json')

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/") # return HttpResponseRedirect('/')