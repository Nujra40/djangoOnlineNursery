import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Details
import time
import random
from dbase import (
    getAuth,
    getCsrf
)

def generateOrderNo(seq_no):
    sequence_no = str(seq_no).zfill(5)
    timestamp = int(time.time())
    random_component = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

    order_number = f"ORDTON-{sequence_no}-{timestamp}-{random_component}"
    return order_number

def deleteProduct(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        if (
            data["user"] == "tatwamasi.admin" and
            data["csrf"] == getCsrf(data["user"]) and
            data["auth"] == getAuth(data["user"])
        ):
            _product = Details.objects.get(id=data["id"])
            _product.delete()
            
            return JsonResponse({
                "status": "delete-success"
            })
            
            
    return JsonResponse({
        "status": "delete-failed"
    })


# Create your views here.
def setDetails(request):

    if(request.method == 'POST'):
        data = json.loads(request.body.decode())
        
        Name = data["name"]
        Sname = data["sname"]
        Price = data["price"]
        Type = data["type"]
        Img = data["img"]
        Properties = data["properties"]
        InitialQ = data["initialQuantity"]
        Quantity = data["quantity"]
        AddToCart = data["addToCart"]

        DatabaseObject = Details()
        DatabaseObject.Name = Name
        DatabaseObject.Scientific_Name = Sname
        DatabaseObject.Price = Price
        DatabaseObject.type = Type
        DatabaseObject.Properties = Properties
        DatabaseObject.Img_path = Img
        DatabaseObject.Initial_quantity = InitialQ
        DatabaseObject.Quantity = Quantity
        DatabaseObject.Add_to_cart = AddToCart 
        DatabaseObject.save()
        
        return JsonResponse({
            "status": "success"
        })
    
    else:
        return JsonResponse({
            "status": "failure"
        })
    
def getDetails(request):
    
    if (request.method == 'POST'):
        Data = Details.objects.all()
        data_list = list(Data.values())
        clientMessage = json.loads(request.body.decode())
        if clientMessage["message"] == "send":
            return JsonResponse({
                "plantDetails": data_list,
                "status": "success"})
        else:
            return JsonResponse({
                "status": "failure"
            })
    
    else:
        return JsonResponse({"status": "failure"})
    
def update(request):
    if (request.method == 'POST'):

        data = json.loads(request.body.decode())
        if(data["admin_mail"] == "tatwamasi.admin"):
            if(data["auth"] == getAuth(data["admin_mail"]) and data["csrf"] == getCsrf(data["admin_mail"])):
                DatabaseObject = Details.objects.get(id=data["id"])
                DatabaseObject.Name = data["update_name"]
                DatabaseObject.type = data["update_type"]
                DatabaseObject.Properties = data["update_properties"]
                DatabaseObject.Price = data["update_price"]
                DatabaseObject.Scientific_Name = data["update_sname"]
                DatabaseObject.save()

                return JsonResponse({
                    "status": "Updated"
                })
            else:
                return JsonResponse({
                    "status": "Authentication_Failed"
                })

        else:
            return JsonResponse({
                "status": "Invalid"
            })

    else:
        return JsonResponse({"status": "Failure"})
