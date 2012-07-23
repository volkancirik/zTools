import string
import random
from sms.models import Shipment

def getTotalShipmentItemCount(request):
    count = 0
    for si in request.session.get("siList",[]):
        count += si.quantity_ordered

    return count

def generateShipmentString():

    first_letter = random.choice(string.letters).upper()
    second_letter = random.choice(string.letters).upper()
    numbers = str(random.randint(0,9999))

    shipment_string = first_letter + second_letter + numbers

    while isNotUnique(shipment_string):
        first_letter = random.choice(string.letters).upper()
        second_letter = random.choice(string.letters).upper()
        numbers = str(random.randint(0,9999))

        shipment_string = first_letter + second_letter + numbers

    return shipment_string

def isNotUnique(shipment_string):
    shipment = Shipment.objects.filter(number=shipment_string)
    if shipment:
        return True
    else:
        return False
