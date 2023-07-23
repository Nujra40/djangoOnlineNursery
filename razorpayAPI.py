import razorpay
import hmac, hashlib

razorpayKeyId = "rzp_test_1cVlhv1wrmqNK9"
razorpayKeySecret = "PG3mWtfVWBHZc0TUFuz2zZ69"
client = razorpay.Client(auth=(razorpayKeyId, razorpayKeySecret))

def createNewOrder(DATA):
    return client.order.create(data=DATA)

def verifyPayment(verifyRequest):
    print(verifyRequest["razorpay_order_id"])
    _signature = hmac.new(
        key=razorpayKeySecret.encode(),
        msg=(verifyRequest["razorpay_order_id"] + "|" + verifyRequest["razorpay_payment_id"]).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if _signature == verifyRequest["razorpay_signature"]:
        return True
    return False