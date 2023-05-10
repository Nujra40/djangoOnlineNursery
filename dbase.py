import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["OnlineNursery"]

users = db["users"]

def authenticate(user):
    user = users.find(user)
    if len(list(user)) == 1:
        return True
    
    return False

def isPresent(user):
    user = users.find({
        "user": user["user"]
    })

    if len(list(user.clone())) == 0:
        return -1
    
    return user.next()["salt"]

def add(user):
    users.insert_one(user)