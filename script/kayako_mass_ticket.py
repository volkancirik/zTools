from kayako import KayakoAPI
from kayako import Ticket, TicketAttachment, TicketNote, TicketPost, TicketPriority, TicketStatus, TicketType, Department
from kayako.objects.user import User
from xlrd import open_workbook

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

        # The user is registered in Kayako but this function return None
        user = api.first(User,email="alp.ozenalp@rocket-internet.com.tr")

        dep = api.first(Department, title=t['department'])
        ticket_type= None
        for ttype in ticketTypeList:
            if ttype.title == t['ticket_type']:
                ticket_type = ttype
                break
        if ticket_type is None:
            ticket_type = ticketTypeList[0]

        ticket = api.create(Ticket, tickettypeid=1, ticketstatusid=1, ticketpriorityid=1, departmentid=13,userid=user.id)
        ticket.subject = t['subject']
        ticket.fullname = t['fullname']
        ticket.email = t['email']
        ticket.contents = t['content']
        ticket.contents = t['type']
        ticket.add()

        print ticket

def readExcel():
    book = open_workbook('mass_ticket_list.xls',encoding_override='utf-8')
    sheet = book.sheet_by_index(0)

    ticketList = []
    for rownum in range(1,4):
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