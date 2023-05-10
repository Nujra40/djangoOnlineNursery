from django.http import JsonResponse

import random
from hashlib import sha256
import json

from dbase import (
    authenticate,
    isPresent,
    add
)

# Create your views here.
def authAPILogin(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode())

        salt = isPresent(user)
        if salt != -1:
            password_salted_sha256 = sha256((salt + user["password"]).encode()).hexdigest()
            _user = {
                "user": user["user"],
                "password_salted_sha256": password_salted_sha256
            }
            if authenticate(_user):
                return JsonResponse({
                    "authAPILogin-response": True
                })
    
    return JsonResponse({
        "authAPILogin-response": False
    })

def authAPISignUp(request):
    if request.method == "POST":
        user = json.loads(request.body.decode())
        
        if isPresent(user) == -1:
            salt = str(int(random.random() * 1000000))
            password_salted_sha256 = sha256((salt + user["password"]).encode()).hexdigest()
            _user = {
                "user": user["user"],
                "salt": salt,
                "password_salted_sha256": password_salted_sha256
            }
            add(_user)
            return JsonResponse({
                "authAPISignUp-response": True
            })
    
    return JsonResponse({
        "authAPISignUp-response": False
    })

