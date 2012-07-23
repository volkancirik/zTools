def getTotalShipmentItemCount(request):
    count = 0
    for si in request.session.get("siList",[]):
        count += si.quantity_ordered

    return count