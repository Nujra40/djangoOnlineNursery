from django.http import JsonResponse
import json
from dbase import (
    pendingOrders,
    orderHistory,
    _updateDeliveryStatus
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
                    if order["status"] != "Order Fulfilled":
                        order["user"] = user["user"]
                        order["name"] = user["fname"] + " " + user["lname"]
                        for product in order["order_details"]:
                            order["order_details"][product]["name"] = Details.objects.get(id=product).Name
                        _p.append(order)
        
        return JsonResponse({"pending-orders": _p})
    
    return JsonResponse({})

def getAllOrders(request):
    if request.method == "POST":
        _req = json.loads(request.body.decode())
        admin = _req["user"]

        if admin != 'tatwamasi.admin':
            return JsonResponse({})
        
        authToken = _req["auth"]
        segment = int(_req["segment"])
        _o = []
        _orderHistory = orderHistory(admin, authToken)
        if _orderHistory is not None:
            for user in _orderHistory:
                if "order_list" not in user: continue
                for order in user["order_list"]:
                    if order["status"] == "Order Fulfilled":
                        order["user"] = user["user"]
                        order["name"] = user["fname"] + " " + user["lname"]
                        for product in order["order_details"]:
                            order["order_details"][product]["name"] = Details.objects.get(id=product).Name
                        _o.append(order)
        

        _o.sort(key=lambda x: x["order_no"].split("-")[2], reverse=True)
        _o = _o[segment * 8: segment * 8 + 8]

        return JsonResponse({"order-history": _o})

    return JsonResponse({})

def updateStatus(request):
    if request.method == "POST":
        _req = json.loads(request.body.decode())
        admin = _req["user"]

        if admin != 'tatwamasi.admin':
            return JsonResponse({})
        
        authToken = _req["auth"]
        if _updateDeliveryStatus(admin, authToken, _req["order_no"], _req["update_message"]):
            return JsonResponse({"updateStatus": "success"})
        
    return JsonResponse({})
