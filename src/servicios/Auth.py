from datetime import datetime
from functools import update_wrapper
from typing import Any

from cryptography.fernet import Fernet
from flask import session, Response, request

from src.negocio.CodigosRespuesta import NO_AUTORIZADO, PROHIBIDO
from src.negocio.MiembroOfercompas import MiembroOfercompas


class Auth:
    secret_password: bytes = None

    @staticmethod
    def set_password():
        Auth.secret_password = Fernet.generate_key()

    @staticmethod
    def requires_token(operation):
        def verify_auth(*args, **kwargs):
            token = request.headers.get("Token")
            try:
                saved_token = session["token"]
            except KeyError:
                saved_token = None
            print(token)
            print(saved_token)
            if token is not None and saved_token is not None and token == saved_token:
                response = operation(*args, **kwargs)
            else:
                response = Response(status=NO_AUTORIZADO)
            return response

        return update_wrapper(verify_auth, operation)

    @staticmethod
    def requires_role(role: Any):
        def decorator(operation):
            def verify_role(*args, **kwargs):
                token = request.headers.get("Token")
                if token is not None:
                    values = Auth.decode_token(token)
                    if str(values["is_owner"]) == str(role):
                        response = operation(*args, **kwargs)
                    else:
                        response = Response(status=PROHIBIDO)
                else:
                    response = Response(status=PROHIBIDO)
                return response

            return update_wrapper(verify_role, operation)

        return decorator

    @staticmethod
    def generate_token(miembro_ofercompas: MiembroOfercompas) -> str:
        if Auth.secret_password is None:
            Auth.set_password()
        timestamp = datetime.now().strftime("%H:%M:%S")
        value: str = miembro_ofercompas.email + "/" + str(int(miembro_ofercompas.is_owner)) + "/" + timestamp
        return Auth.encode(value, Auth.secret_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = Auth.decode(token, Auth.secret_password)
        decoded_token = decoded_token.split("/")
        return {
            "email": decoded_token[0],
            "is_owner": decoded_token[1]
        }

    @staticmethod
    def decode(value: str, key: bytes) -> str:
        return Fernet(key).decrypt(value.encode()).decode()

    @staticmethod
    def encode(value: str, key: bytes) -> str:
        return Fernet(key).encrypt(value.encode()).decode()