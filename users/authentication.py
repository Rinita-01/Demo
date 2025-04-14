import jwt
from datetime import datetime, timedelta, timezone
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from users.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.get(pk=id)
            return (user, {'is_admin': user.is_superuser})
        raise exceptions.AuthenticationFailed('unauthenticated')

def create_access_token(id):
    payload = {
        'user_id': id,
        'iat': datetime.now(timezone.utc),  
        'exp': datetime.now(timezone.utc) + timedelta(seconds=30),  # Expiration time (Current time + 30 seconds), timedelta(seconds=5)  
    }
    secret_key = "access_secret"
    algorithm = "HS256"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def create_refresh_token(id):
    payload = {
        'user_id': id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),  
        'iat': datetime.now(timezone.utc)
    }
    secret_key = "refresh_secret"
    algorithm = "HS256"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')
        print(f'payload: {payload}')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')