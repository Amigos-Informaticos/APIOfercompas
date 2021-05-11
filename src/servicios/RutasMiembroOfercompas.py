import json

from flask import Blueprint, request, Response

from src.negocio.MiembroOfercompas import MiembroOfercompas

rutas_miembro = Blueprint("rutas_miembro", __name__)


@rutas_miembro.route("/miembros", methods=["POST"])
def registrar_miembro():
    miembro_recibido = request.json
    valores_requeridos = {"email", "nickname", "contrasenia"}
    respuesta = Response(status=400)
    if miembro_recibido is not None:
        if all(llave in miembro_recibido for llave in valores_requeridos):
            miembro = MiembroOfercompas()
            miembro.email = miembro_recibido["email"]
            miembro.contrasenia = miembro_recibido["contrasenia"]
            miembro.nickname = miembro_recibido["nickname"]
            resultado = miembro.registrar()
            if resultado == 0:
                respuesta = Response(
                    json.dumps({
                        "idMiembro": miembro.idMiembro,
                        "email": miembro.email,
                        "contrasenia": miembro.contrasenia,
                        "nickname": miembro.nickname,
                        "estado": miembro.estado,
                        "tipoMiembro": miembro.tipoMiembro
                    }),
                    status=201,
                    mimetype="application/json"
                )
            elif resultado == 1:
                respuesta = Response(status=409)
            elif resultado == 2:
                respuesta = Response(status=500)
    else:
        respuesta = Response(status=400)

    return respuesta


@rutas_miembro.route("/miembros/<old_email>", methods=["PUT"])
def actualizar_miembro(old_email):
    valores_requeridos = {"email", "nickname", "contrasenia"}
    miembro_recibido = request.json
    respuesta = Response(200)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.email = miembro_recibido["email"]
        miembro.contrasenia = miembro_recibido["contrasenia"]
        miembro.nickname = miembro_recibido["nickname"]
        resultado = miembro.actualizar_miembro(old_email)
        if resultado == 0:
            respuesta = Response(
                json.dumps({
                    "idMiembro": miembro.idMiembro,
                    "email": miembro.email,
                    "contrasenia": miembro.contrasenia,
                    "nickname": miembro.nickname,
                    "estado": miembro.estado,
                    "tipoMiembro": miembro.tipoMiembro
                }),
                status=200,
                mimetype="application/json"
            )
        elif resultado == 1:
            respuesta = Response(status=409)
        elif resultado == 2:
            respuesta = Response(status=500)
        elif resultado == 3:
            respuesta = Response(status=404)
    else:
        respuesta = Response(status=400)
    return  respuesta