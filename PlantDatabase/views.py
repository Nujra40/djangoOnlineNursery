from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Details

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
        print(Data)
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
    
# def addCartUpdate(request):

#     if(request.method == 'POST'):
#         data = json.loads(request.body.decode())
#         id = data["id"]

#         plantDetail = Details.objects.get(id = id)

#         if(plantDetail.Add_to_cart == "Add"):
#             plantDetail.Add_to_cart = "Added"
#         else:
#             plantDetail.Add_to_cart = "Add"
        
#         plantDetail.save()

#         return JsonResponse({"status": "success"})
#     else:
#         return JsonResponse({"status": "failure"})

