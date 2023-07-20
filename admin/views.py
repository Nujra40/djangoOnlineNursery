from django.http import JsonResponse
import json
from dbase import (
    pendingOrders
)

# Create your views here.
def getAllOrders(request):

    return JsonResponse()

def getPendingOrders(request):
    if request.method == "POST":
        _request = json.loads(request.body.decode())
        admin = _request["user"]
        
        if admin != 'tatwamasi.admin':
            return JsonResponse({})
        
        authToken = _request["auth"]
        _p = []
        _pendingOrders = pendingOrders(admin, authToken)
        if _pendingOrders is not None:
            for user in _pendingOrders:
                for order in user["order_list"]:
                    if order["status"] == "Order Placed":
                        order["user"] = user["user"]
                        _p.append(order)
        
        return JsonResponse({"pending-orders": _p})
    
    return JsonResponse({})