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

def verifyOTP(_user):
    user = temp.find({
        "user": _user["user"]
    })

    if len(list(user.clone())) == 0:
        return False
    
    return user.next()["otp"] == _user["otp"]

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