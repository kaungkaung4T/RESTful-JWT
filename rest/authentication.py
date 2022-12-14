import jwt
import datetime
from rest_framework import exceptions


def access_encode(user):
    payload = {
        "username": user.username,
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, "access_secret", "HS256")


def access_decode(token):
    try:
        payload = jwt.decode(token, "access_secret", algorithms="HS256")
        return payload["user_id"]

    except Exception as e:
        raise exceptions.AuthenticationFailed("unauthenticated")


def refresh_encode(user):
    payload = {
        "username": user.username,
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=40),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, "refresh_secret", algorithm="HS256")


def refresh_decode(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms="HS256")
        return payload["user_id"]
    except Exception as e:
        raise exceptions.AuthenticationFailed("unauthenticated")

