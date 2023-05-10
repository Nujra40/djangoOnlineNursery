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
        if user["alt"] == "":
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
