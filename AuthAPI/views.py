from django.http import JsonResponse

import random
import time
from hashlib import sha256
import json
import datetime

from mail.mail import sendMail
import razorpayAPI


SERVER_SECRET = "8255d89e73529ed5b9879e1921c06661d8ea817198071913817b6d9a3561f9a2"
OAuth2_KEY = "829309063059-62n8osovkljiguccn24fmt2kmeaoohf9.apps.googleusercontent.com"

from dbase import (
    authenticate,
    isPresent,
    add,
    addAlt,
    addTemp,
    verifyOTP,
    delTemp,
    verifyAuthToken,
    updateCSRF,
    verifyCSRF,
    updateAuthToken,
    getAuthToken,
    setOTP,
    updatePassword,
    addPlant,
    removePlant,
    getCartPlants,
    incQuantity,
    decQuantity,
    getUserDetails,
    saveUserDetails,
    placeOrder,
    getOrderList
)

sequence_no = "1"

def genAuthToken():
    _token = ""

    for i in range(64):
        _token += random.choice("0123456789abcdef")
    
    return _token

def genCSRF(user):
    _token = genAuthToken()

    return (updateCSRF({
        "user": user["email/phone"],
        "csrf": _token
    }), _token)

def _authenticate(user):
    
    user["user"] = user["email/phone"]
    if user["user"] == "":
        return False

    if "authToken" in user and user["authToken"] != "":
        if "csrf" in user and user["csrf"] != "":
            return verifyAuthToken(user) and verifyCSRF(user)
    
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

        print(user)

        if _authenticate(user):
            updateCSRF({
                "user": user["user"],
                "csrf": SERVER_SECRET
            })

            authToken = ""
            if "authToken" not in user:
                aU = getAuthToken(user)
                if aU == '':
                    authToken = genAuthToken()
                else:
                    authToken = aU
                updateAuthToken({
                    "user": user["user"],
                    "authToken": authToken 
                })
            
            return JsonResponse({
                "authAPILogin-response": "Success",
                "authToken": authToken
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
            updateCSRF({
                "user": user["user"],
                "csrf": SERVER_SECRET
            })
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
                otp = str(int(random.random() * 10000))
                sendMail(user["user"], user["fname"], otp)
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
            authToken = genAuthToken()
            _user = {
                "user": user["user"],
                "salt": salt,
                "password_salted_sha256": password_salted_sha256,
                "fname": user["fname"],
                "lname": user["lname"],
                "alt": "",
                "authToken": authToken
            }
            add(_user)
            delTemp(_user)
            res = JsonResponse({
                "authAPISignUp-response": "Success",
                "authToken": authToken
            })
            return res
    
    return JsonResponse({
        "authAPISignUp-response": "Failed"
    })

def authAPIgetCSRF(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())

        res = genCSRF(user)
        if res[0]:
            return JsonResponse({
                "csrf": res[1]
            })
    
    return JsonResponse({
        "csrf": "Invalid User"
    })

def authAPIforgotPassword(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())

        user["user"] = user["email/phone"]

        salt = isPresent(user)
        if salt != -1:
            if "otp" in user:
                if verifyOTP(user, collection="users"):
                    if "new-password" in user:
                        password_salted_sha256 = sha256((salt + user["new-password"]).encode()).hexdigest()
                        updatePassword(user, password_salted_sha256)
                        setOTP(user, SERVER_SECRET)

                        return JsonResponse({
                            "authAPIforgotPassword-response": "Password Changed"
                        })

                    return JsonResponse({
                        "authAPIforgotPassword-response": "Matched"
                    })
                
                else:
                    return JsonResponse({
                        "authAPIforgotPassword-response": "Failed"
                    })

            otp = str(int(random.random() * 10000))
            sendMail(user["user"], setOTP(user, otp), otp)
        
            return JsonResponse({
                "authAPIforgotPassword-response": "OTP Verification Required"
            })
        
    return JsonResponse({
        "authAPIforgotPassword-response": "Failed"
    })

def authAPIOAuth2(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())

        if not user["OAuth2_key"] == OAuth2_KEY:
            return JsonResponse({
                "authAPIOAuth2-response": "Failed"
            })
        
        user["user"] = user["email"]
        user["email/phone"] = user["email"]
        user["password"] = user["name"] + user["sub"] + user["email"] + SERVER_SECRET

        salt = isPresent(user)
        if salt != -1:

            if _authenticate(user):
                authToken = genAuthToken()
                updateAuthToken({
                    "user": user["user"],
                    "authToken": authToken
                })

                return JsonResponse({
                    "authAPIOAuth2-response": "Success",
                    "authToken": authToken
                })
            
            return JsonResponse({
                "authAPIOAuth2-response": "Failed"
            })
        
        salt = str(int(random.random() * 1000000))
        password_salted_sha256 = sha256((salt + user["password"]).encode()).hexdigest()
        authToken = genAuthToken()
        _user = {
            "user": user["user"],
            "salt": salt,
            "password_salted_sha256": password_salted_sha256,
            "fname": user["name"].split()[0],
            "lname": user["name"].split()[-1],
            "alt": "",
            "authToken": authToken
        }
        add(_user)
        return JsonResponse({
            "authAPIOAuth2-response": "Success",
            "authToken": authToken
        })

def generateOrderNo(seq_no):
    sequence_no = str(seq_no).zfill(5)
    timestamp = int(time.time())
    random_component = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

    order_number = f"ORDTON-{sequence_no}-{timestamp}-{random_component}"
    return order_number

def userFunction(request):
    global sequence_no
    if(request.method == "POST"):
        data = json.loads(request.body.decode())
        if(data["function"] == "send user details"):
            user_details = getUserDetails(data["email"])
            return JsonResponse({"status": "success", "user_details": user_details})
        
        if(data["function"] == "save changes"):
            if(saveUserDetails(data["email"], data["username"], data["auth"])):
                return JsonResponse({"status": "saved"})
            else:
                return JsonResponse({"status": "error"})
            
        elif(data["function"] == "place order"):
            sequence_no = str(int(sequence_no) + 1)
            if razorpayAPI.verifyPayment(data["orders"]):
                if(placeOrder(data["email"], generateOrderNo(sequence_no.zfill(5)), str(datetime.date.today()), data["orders"], data["auth"])):
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "failed"})
        
        elif(data["function"] == "send order list"):
            order_list = getOrderList(data['email'])
            order_list.reverse()
            if(order_list):
                return JsonResponse({"order_list": order_list, "status": "success"})
            else:
                return JsonResponse({"status": "failed"})

        else:
            return JsonResponse({"status": "failed"})


def cartFunction(request):

    if(request.method == "POST"):
        data = json.loads(request.body.decode())
        if(data["function"] == "add"):
            if(addPlant(data["email"], data["plant_id"])):
                return JsonResponse(
                    {"status": "plant added"},
                )
            else:
                return JsonResponse({"status": "failed"})
            
        elif(data["function"] == "remove"):
            if(removePlant(data["email"], data["plant_id"])):
                return JsonResponse(
                    {"status": "plant removed"},
                )
            else:
                return JsonResponse({"status": "failed"})
            
        elif(data["function"] == "send cart details"):
            
            return JsonResponse({
                "cart_plants": getCartPlants(data["email"])
            })
        
        elif(data["function"] == "increment"):
            if(incQuantity(data["email"], data["plant_id"])):
                return JsonResponse({
                    "status": "incremented"
                })
            else:
                return JsonResponse({"status": "failed"})
            
        elif(data["function"] == "decrement"):
            if(decQuantity(data["email"], data["plant_id"])):
                return JsonResponse({
                    "status": "decremented"
                })
            else:
                return JsonResponse({"status": "failed"})
            
    else:
        return JsonResponse({"status": "failed"})
        
