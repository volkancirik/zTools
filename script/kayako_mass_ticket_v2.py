import socket
import urllib

import hashlib
import random
import base64
import urllib
import hmac
import sys


def createTicket():

    apikey = "337f1965-2b4c-5494-bde9-144a50e90534"
    secretkey = "NjhkN2Y5MTMtOTUzNy1lZGY0LWM5NWMtZGVkMDJkZmRlNjczZDQwZmYwNWUtZGIxMy01Nzk0LTE5NmYtNDZhMzg5ZGIyZmFm"


    # Generates a random string of ten digits
    salt = str(random.getrandbits(32))

    # Computes the signature by hashing the salt with the secret key as the key
    signature = hmac.new(secretkey, msg=salt, digestmod=hashlib.sha256).digest()

    # base64 encode...
    encodedSignature = base64.encodestring(signature).replace('\n', '')

    # urlencode...
    encodedSignature = urllib.quote(encodedSignature)

    subject = 'TEST - Do not take action'
    fullname = 'Baris Bilgic Test User'
    email = 'brsbilgic@gmail.com'
    contents = 'There is going to be some order numbers and customer name etc.'

    API_URL = 'https://customersupport.rocket-internet.com.tr/api/index.php?apikey=%s&salt=%s&signature=%s'%(apikey,salt,signature)

    post_parameters = {
                           "subject":subject,
                           "fullname":fullname,
                           "email":email,
                           "contents":contents,
                           "departmentid":13,
                           "ticketstatusid":1,
                           "ticketpriorityid":1,
                           "autouserid":1}

    params = urllib.urlencode(post_parameters)

    timeout = 50
    socket.setdefaulttimeout(timeout)

    try:
        res = urllib.urlopen(API_URL,params)
    except:
        e = sys.exc_info()[1]
        print e

    print res


createTicket()