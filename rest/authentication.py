import jwt
import datetime


def access_encode(id):
    payload = {
        "id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, "secret", algorithm="HS256")


def access_decode(token):
    payload = jwt.decode(token, "secret", algorithm="HS256")

    return payload["id"]


def refresh_encode(id):
    pass









