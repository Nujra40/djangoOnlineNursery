import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Details
import time
import random

def generateOrderNo(seq_no):
    sequence_no = str(seq_no).zfill(5)
    timestamp = int(time.time())
    random_component = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

    order_number = f"ORDTON-{sequence_no}-{timestamp}-{random_component}"
    return order_number



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

        Obj = Details()
        Obj.Name = Name
        Obj.Scientific_Name = Sname
        Obj.Price = Price
        Obj.type = Type
        Obj.Properties = Properties
        Obj.Img_path = Img
        Obj.Initial_quantity = InitialQ
        Obj.Quantity = Quantity
        Obj.Add_to_cart = AddToCart 
        Obj.save()
        
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
            Obj = Details.objects.get(id=data["id"])
            Obj.Name = data["up_name"]
            Obj.type = data["up_type"]
            Obj.Properties = data["up_properties"]
            Obj.Price = data["up_price"]
            Obj.Scientific_Name = data["up_sname"]
            Obj.save()
            print(Obj.Name)

            return JsonResponse({
                "status": "updated"
            })

        else:
            return JsonResponse({
                "status": "invalid email"
            })

    else:
        return JsonResponse({"status": "failure"})
    

    

    


