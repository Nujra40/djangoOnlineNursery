from django.http import JsonResponse
import json
from dbase import (
    pendingOrders,
    orderHistory
)

from PlantDatabase.models import Details

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
                        for product in order["order_details"]:
                            order["order_details"][product]["name"] = Details.objects.get(id=product).Name
                        _p.append(order)
        
        return JsonResponse({"pending-orders": _p})
    
    return JsonResponse({})

def getAllOrders(request):
    if request.method == "POST":
        _req = json.loads(request.body.decode())
        admin = request["user"]

        if admin != 'tatwamasi.admin':
            return JsonResponse({})
        
        authToken = _req["auth"]
        _o = []
        _orderHistory = orderHistory(admin, authToken, request["segment"])
        if _orderHistory is not None:
            for user in _orderHistory:
                for order in user["order_list"]:
                    if order["status"] == "Order Placed":
                        order["user"] = user["user"]
                        order["name"] = user["fname"] + " " + user["lname"]
                        for product in order["order_details"]:
                            order["order_details"][product]["name"] = Details.objects.get(id=product).Name
                        _o.append(order)

        return JsonResponse({"order-history": _o})

    return JsonResponse({})
