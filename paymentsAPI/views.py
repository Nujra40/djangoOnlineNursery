from django.http import JsonResponse

import json
import razorpayAPI

def createNewOrder(request):
    if request.method == "POST":
        orderRequest = json.loads(request.body.decode())
        return JsonResponse(razorpayAPI.createNewOrder({
            'amount': orderRequest['amount'],
            "currency": "INR"
        }))
    
    return JsonResponse({"status": "razorpay-order-error"})

def verifyPayment(request):
    if request.method == "POST":
        verifyRequest = json.loads(request.body.decode())
        if razorpayAPI.verifyPayment(verifyRequest):
            return JsonResponse({
                "status": "razorpay-payment-signature-verified"
            })
    
    return JsonResponse({"status": "razorpay-payment-error"})
