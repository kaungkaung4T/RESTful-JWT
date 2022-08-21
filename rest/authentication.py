import jwt
import datetime
from rest_framework import exceptions

def access_encode(user):
    payload = {
        "name": user.username,
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, "a secret", algorithm="HS256")


def access_decode(token):
    try:
        payload = jwt.decode(token, "a secret", algorithms="HS256")
        return payload["id"]

    except Exception as e:
        raise exceptions.AuthenticationFailed("unauthenticated")


def refresh_encode(user):
    payload = {
        "name": user.username,
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=40),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, "r secret", algorithm="HS256")


def refresh_decode(token):
    try:
        payload = jwt.decode(token, "r secret", algorithms="HS256")
        return payload["id"]
    except Exception as e:
        raise exceptions.AuthenticationFailed("unauthenticated")

