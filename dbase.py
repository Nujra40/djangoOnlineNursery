import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["OnlineNursery"]

users = db["users"]
temp = db["temp"]

def authenticate(user):
    user = users.find(user)
    if len(list(user)) == 1:
        return True
    
    return False

def isPresent(_user):
    user = users.find({
        "user": _user["user"]
    })

    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(user.clone())) == 0:
        if len(list(alt.clone())) == 0:
            return -1
        
        else:
            return alt.next()["salt"]
    else:
        return user.next()["salt"]

def add(user):
    users.insert_one(user)

def addAlt(_user):
    user = users.find({
        "user": _user["user"]
    })

    if len(list(user.clone())) != 0:
        user = user.next()
        users.update_one(
            { "user": _user["user"] },
            { "$set": {
                    "alt": _user["alt"]
                }
            }
        )
        
        return True
        
    return False

def addTemp(_user):
    temp.delete_many({
            "user": _user["user"]
    })
    
    temp.insert_one(_user)

def verifyOTP(_user, collection="temp"):
    if collection == "temp":
        collection = temp
    else:
        collection = users

    user = collection.find({
        "otp": _user["otp"]
    })

    if len(list(user.clone())) == 1:
        user = user.next()
        if user["user"] == _user["user"] or user["alt"] == _user["user"]:
            return True
        
    return False

def delTemp(_user):
    temp.delete_many({
        "user": _user["user"]
    })

def verifyAuthToken(_user):
    user = users.find({
        "authToken": _user["authToken"]
    })

    if len(list(user.clone())) == 1:
        user = user.next()
        if user["user"] == _user["user"] or user["alt"] == _user["user"]:
            return True
    
    return False

def updateCSRF(_user):
    user = users.find({
        "user": _user["user"]
    })

    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(user.clone())) == 0:
        if len(list(alt.clone())) == 0:
            return False
        
        else:
            users.update_one(
                { "alt": _user["user"] },
                { "$set": {
                        "csrf": _user["csrf"]
                    }
                }
            )
            return True
    else:
        users.update_one(
            { "user": _user["user"] },
            { "$set": {
                    "csrf": _user["csrf"]
                }
            }
        )
        return True

def updateAuthToken(_user):
    user = users.find({
        "user": _user["user"]
    })

    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(user.clone())) == 0:
        if len(list(alt.clone())) == 0:
            return False
        
        else:
            users.update_one(
                { "alt": _user["user"] },
                { "$set": {
                        "authToken": _user["authToken"]
                    }
                }
            )
            return True
    else:
        users.update_one(
            { "user": _user["user"] },
            { "$set": {
                    "authToken": _user["authToken"]
                }
            }
        )
        return True

def verifyCSRF(_user):
    user = users.find({
        "csrf": _user["csrf"]
    })

    if len(list(user.clone())) == 1:
        user = user.next()
        if user["user"] == _user["user"] or user["alt"] == _user["user"]:
            return True
    
    return False

def getAuthToken(_user):
    user = users.find({
        "user": _user["user"]
    })

    if len(list(user.clone())) == 1:
        return user.next()["authToken"]
    
    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(alt.clone())) == 1:
        return alt.next()["authToken"]
    
    return ""

def setOTP(_user, otp):
    user = users.find({
        "user": _user["user"]
    })

    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(user.clone())) == 0:
        if len(list(alt.clone())) == 0:
            return False
        
        else:
            users.update_one(
                { "alt": _user["user"] },
                { "$set": {
                        "otp": otp
                    }
                }
            )
            return alt.next()["fname"]
    else:
        users.update_one(
            { "user": _user["user"] },
            { "$set": {
                    "otp": otp
                }
            }
        )
        return user.next()["fname"]

def updatePassword(_user, password_salted_sha256):
    user = users.find({
        "user": _user["user"]
    })

    alt = users.find({
        "alt": _user["user"]
    })

    if len(list(user.clone())) == 0:
        if len(list(alt.clone())) == 0:
            return False
        
        else:
            users.update_one(
                { "alt": _user["user"] },
                { "$set": {
                        "password_salted_sha256": password_salted_sha256
                    }
                }
            )
            return True
    else:
        users.update_one(
            { "user": _user["user"] },
            { "$set": {
                    "password_salted_sha256": password_salted_sha256
                }
            }
        )
        return True
    
def getCsrf(_user):
    user = users.find_one({
        "user": _user
    })

    if user:
        csrf = user.get("csrf")
        return csrf
    
    return None

def getAuth(_user):
    user = users.find_one({
        "user": _user
    })
    print(_user)

    if user:
        auth = user.get("authToken")
        return auth
    
    return None
    
def addPlant(_email, _plantId):
    user = users.find_one({
        "user": _email
    })

    if user:
        cart_plants = user.get("cart_plants", {})
        if str(_plantId) not in cart_plants:
            cart_plants[str(_plantId)] = [1, "Added"]
            users.update_one(
                {"user": _email},
                {"$set": {
                    "cart_plants": cart_plants
                    }
                }
            )
            return True
        else:
            return False
    else:
        return False
    
def removePlant(_email, _plantId):
    user = users.find_one({
        "user": _email
    })

    if user:
        cart_plants = user.get("cart_plants")
        if str(_plantId) in cart_plants:
            cart_plants.pop(str(_plantId))
            users.update_one(
                {"user": _email},
                {"$set": {
                    "cart_plants": cart_plants
                    }
                }
            )
            return True
        else:
            return False
    else:
        return False
    
def getCartPlants(_email):
    user = users.find_one({
        "user": _email
    })

    if user:
        cart_plants =  user.get("cart_plants")
        print(cart_plants)
        return cart_plants
    
def incQuantity(_email, _plantId):
    user = users.find_one({
        "user": _email
    })

    if user:
        cart_plants = user.get("cart_plants")
        cart_plants[str(_plantId)][0] = cart_plants[str(_plantId)][0] + 1
        users.update_one(
            {"user": _email},
            {"$set": {"cart_plants": cart_plants}}
        )
        return True
    else:
        return False
    
def decQuantity(_email, _plantId):
    user = users.find_one({
        "user": _email
    })

    if user:
        cart_plants = user.get("cart_plants")
        cart_plants[str(_plantId)][0] = cart_plants[str(_plantId)][0] - 1
        if cart_plants[str(_plantId)][0] > 0:
            users.update_one(
                {"user": _email},
                {"$set": {"cart_plants": cart_plants}}
            )
            return True
        else:
            return False
    else:
        return False
    
def getUserDetails(_email):
    user = users.find_one({
        "user": _email
    })

    if user:
        username = user.get("fname")
        user_email = user.get("user")
        return {
            "username": username,
            "email": user_email 
        }
    
    else: 
        return None
    
def saveUserDetails(_email, _username, _auth):
    user = users.find_one({
        "user": _email
    })

    if user:
        auth = user.get("authToken")
        if getAuth(_email) == _auth:
            users.update_one(
                {"user": _email},
                {"$set": {"fname": _username}}
            )
            return True
    
    else:
        return False

def placeOrder(_email, _order_no, _order_date, _order_details, _auth):
    user = users.find_one({
        "user": _email
    })
    amount_paid = _order_details["amount_paid"]
    del _order_details["amount_paid"]
    del _order_details["razorpay_order_id"]
    del _order_details["razorpay_payment_id"]
    del _order_details["razorpay_signature"]
    if user:
        if getAuth(_email) == _auth:
            orders = user.get("order_list", [])
            orders.append({
                "order_no": _order_no,
                "order_date": _order_date,
                "status": "Order Placed",
                "order_details": _order_details,
                "amount_paid": amount_paid
            })
            users.update_one(
                {"user": _email},
                {"$set": {"order_list": orders, "containsPendingOrder": "Yes", "latestOrderDate": _order_date}}
            )
            return True
    
    else: 
        return False

def _updateDeliveryStatus(admin, auth, order_no, update_message):
    _user = {"user": admin, "authToken": auth}
    if verifyAuthToken(_user):
        users.update_one(
            { "order_list.order_no": order_no },
            { "$set": { "order_list.$.status": update_message } }
        )
        return True
    
    return False


def getOrderList(_email):
    user = users.find_one({
        "user": _email
    })

    if user:
        orders = user.get("order_list", [])
        return orders
    
    else:
        return None

def pendingOrders(admin, _auth):
    _user = {"user": admin, "authToken": _auth}
    if verifyAuthToken(_user):
        _pendingOrders = users.find({
            "containsPendingOrder": "Yes"
        })

        return list(_pendingOrders)
    
    return None

def orderHistory(admin, _auth):
    _user = { "user": admin, "authToken": _auth }
    if verifyAuthToken(_user):
        _orderHistory = users.find()
    
        return list(_orderHistory)
    return None
        