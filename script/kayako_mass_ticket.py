import urllib2
from kayako import KayakoAPI
from kayako import Ticket, TicketAttachment, TicketNote, TicketPost, TicketPriority, TicketStatus, TicketType, Department
from kayako.api import log
from kayako.core.lib import UnsetParameter
from kayako.exception import KayakoRequestError, KayakoResponseError
from kayako.objects.user import User
from xlrd import open_workbook
import hashlib
import random
import base64
import urllib
import hmac
import sys

def add(controller,parameters):
        '''
        Add this Ticket.

        Requires:
            subject          The Ticket Subject
            fullname         Full Name of creator
            email            Email Address of creator
            contents         The contents of the first ticket post
            departmentid     The Department ID
            ticketstatusid   The Ticket Status ID
            ticketpriorityid The Ticket Priority ID
            tickettypeid     The Ticket Type ID
        At least one of these must be present:
            userid           The User ID, if the ticket is to be created as a user.
            staffid          The Staff ID, if the ticket is to be created as a staff
        Optional:
            ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
            type             The ticket type: 'default' or 'phone'
        '''
        #if 'userid' not in parameters and 'staffid' not in parameters:
        #    raise KayakoRequestError('To add a Ticket, at least one of the following parameters must be set: userid, staffid. (id: %s)' % self.id)

        response = _request(controller, 'POST', parameters)

def _request(controller, method, parameters):

        api_key = "337f1965-2b4c-5494-bde9-144a50e90534"
        secret_key = "NjhkN2Y5MTMtOTUzNy1lZGY0LWM5NWMtZGVkMDJkZmRlNjczZDQwZmYwNWUtZGIxMy01Nzk0LTE5NmYtNDZhMzg5ZGIyZmFm"
        api_url = 'http://customersupport.rocket-internet.com.tr/api/index.php'

        # Generate random 10 digit number
        salt = str(random.getrandbits(32))
        # Use HMAC to encrypt the secret key using the salt with SHA256
        encrypted_signature = hmac.new(secret_key, msg=salt, digestmod=hashlib.sha256).digest()
        # Encode the bytes into base 64
        b64signature = base64.b64encode(encrypted_signature)

        log.info('REQUEST: %s %s' % (controller, method))

        request = ""
        url=""
        data=""
        if method == 'GET':
            url = '%s?e=%s&apikey=%s&salt=%s&signature=%s' % (api_url, urllib.quote(controller), urllib.quote(api_key), salt, urllib.quote(b64signature))
            # Append additional query args if necessary
            data = _post_data(parameters)
            if data:
                url = '%s&%s' % (url, data)
            request = urllib2.Request(url)
        elif method == 'POST':
            url = '%s?e=%s' % (api_url, urllib.quote(controller))
            # Auth parameters go in the body for these methods
            parameters['apikey'] = api_key
            parameters['salt'] = salt
            parameters['signature'] = b64signature
            data = _post_data(parameters)
            request = urllib2.Request(url, data=data, headers={'Content-length' : len(data) if data else 0})
            request.get_method = lambda: method
        log.debug('REQUEST URL: %s' % url)
        log.debug('REQUEST DATA: %s' % data)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            response_error = KayakoResponseError('%s: %s' % (error, error.read()))
            raise response_error
        except urllib2.URLError, error:
            request_error = KayakoRequestError(error)
            raise request_error
        return response

def _post_data(parameters):
        data = ""
        first = True
        for key, value in parameters.iteritems():
            data += '%s=%s&' % (key, urllib2.quote(value))
        return data

def initKayako():
    API_KEY = '337f1965-2b4c-5494-bde9-144a50e90534'
    API_URL = 'http://customersupport.rocket-internet.com.tr/api/index.php'
    SECRET_KEY = 'NjhkN2Y5MTMtOTUzNy1lZGY0LWM5NWMtZGVkMDJkZmRlNjczZDQwZmYwNWUtZGIxMy01Nzk0LTE5NmYtNDZhMzg5ZGIyZmFm'
    return KayakoAPI(API_URL, API_KEY, SECRET_KEY)

def createTicket(ticketList):
    try:
        api = initKayako()
    except:
        print "Initialization Error"
        return

    ticketTypeList = api.get_all(TicketType)
    
    for t in ticketList:
        
        dep = api.first(Department, title=t['department'])
        ticket_type= None
        for ttype in ticketTypeList:
            if ttype.title == t['ticket_type']:
                ticket_type = ttype
                break
        if ticket_type is None:
            ticket_type = ticketTypeList[0]

        ticket = api.create(Ticket, tickettypeid=1, ticketstatusid=1, ticketpriorityid=1, departmentid=13)
        ticket.subject = t['subject']
        ticket.fullname = t['fullname']
        ticket.email = t['email']
        ticket.contents = t['content']
        try:
            parameters = {
                'subject':t['subject'].encode('utf-8'),
                'fullname':t['fullname'].encode('utf-8'),
                'email':t['email'],
                'contents':t['content'].encode('utf-8'),
                'departmentid':str(dep.id),
                'ticketstatusid':'1',
                'ticketpriorityid':'1',
                'tickettypeid':str(ticket_type.id),
                'autouserid':'1',
                'templategroup':t['department'],
                'type':t['type'],
            }
            add('/Tickets/Ticket/Create',parameters)
        except:
            e = sys.exc_info()[1]
            print e

def readExcel():
    book = open_workbook('mass_ticket_list.xls',encoding_override='utf-8')
    sheet = book.sheet_by_index(0)

    ticketList = []
    for rownum in range(1,5):
        data = {'department':sheet.cell(rownum,0).value,
                'ticket_type':sheet.cell(rownum,1).value,
                'subject':sheet.cell(rownum,2).value,
                'fullname':sheet.cell(rownum,3).value,
                'email':sheet.cell(rownum,4).value,
                'content':sheet.cell(rownum,5).value,
                'type':sheet.cell(rownum,6).value}
        ticketList.append(data)

    createTicket(ticketList)


readExcel()
#createTicket()