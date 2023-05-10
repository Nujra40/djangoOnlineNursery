from django.http import JsonResponse

import random
from hashlib import sha256
import json

from dbase import (
    authenticate,
    isPresent,
    add,
    addAlt,
    addTemp,
    verifyOTP,
    delTemp
)

def _authenticate(user):
    
    user["user"] = user["email/phone"]
    
    salt = isPresent(user)
    if salt != -1:
        password_salted_sha256 = sha256((salt + user["password"]).encode()).hexdigest()
        _user = {
            "user": user["user"],
            "password_salted_sha256": password_salted_sha256
        }

        __user = {
            "alt": user["user"],
            "password_salted_sha256": password_salted_sha256
        }

        if authenticate(_user) or authenticate(__user):
            return True
    
    return False

# Create your views here.
def authAPILogin(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode())

        if _authenticate(user):
            return JsonResponse({
                "authAPILogin-response": "Success"
            })

    return JsonResponse({
        "authAPILogin-response": "Failed"
    })


'''
    request.POST --> {
        "email/phone": value,
        "fname": value,
        "lname": value,
        "password": value
    }

    Table Contains ---> {
        user,
        password_salted_sha256,
        salt,
        fname,
        lname,
        alt
    }
'''

def authAPIAddAlt(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())
        

        if _authenticate(user):
            
            user["user"] = user["email/phone"]
            if addAlt(user):
                return JsonResponse({
                    "authAPIAddAlt-response": "Success"
                })

    return JsonResponse({
        "authAPIAddAlt-response": "Failed"
    })
        

def authAPISignUp(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())

        user["user"] = user["email/phone"]

        if isPresent(user) == -1:
            if "otp" not in user or user["otp"] == "":
                otp = str(int(random.random() * 1000000))
                user.update({ "otp": otp })
                addTemp(user)
                return JsonResponse({
                    "authAPISignUp-response": "OTP Verification Required"
                })
            
            if not verifyOTP(user):
                return JsonResponse({
                    "authAPISignUp-response": "OTP Verification Failed"
                })
                
            salt = str(int(random.random() * 1000000))
            password_salted_sha256 = sha256((salt + user["password"]).encode()).hexdigest()
            _user = {
                "user": user["user"],
                "salt": salt,
                "password_salted_sha256": password_salted_sha256,
                "fname": user["fname"],
                "lname": user["lname"],
                "alt": ""
            }
            add(_user)
            delTemp(_user)
            return JsonResponse({
                "authAPISignUp-response": "Success"
            })
    
    return JsonResponse({
        "authAPISignUp-response": "Failed"
    })

