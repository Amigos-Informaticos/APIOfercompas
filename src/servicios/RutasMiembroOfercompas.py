import json

from flask import Blueprint, request, Response

from src.negocio import CodigosRespuesta
from src.negocio.MiembroOfercompas import MiembroOfercompas

rutas_miembro = Blueprint("rutas_miembro", __name__)


@rutas_miembro.route("/miembros", methods=["POST"])
def registrar_miembro():
    miembro_recibido = request.json
    valores_requeridos = {"email", "nickname", "contrasenia"}
    respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)
    if miembro_recibido is not None:
        if all(llave in miembro_recibido for llave in valores_requeridos):
            miembro = MiembroOfercompas()
            miembro.email = miembro_recibido["email"]
            miembro.contrasenia = miembro_recibido["contrasenia"]
            miembro.nickname = miembro_recibido["nickname"]
            resultado = miembro.registrar()
            if resultado == CodigosRespuesta.RECURSO_CREADO:
                respuesta = Response(
                    json.dumps(miembro.convertir_a_json(["idMiembro", "email", "contrasenia", "nickname",
                                                         "estado", "tipoMiembros"])),
                    status=CodigosRespuesta.RECURSO_CREADO,
                    mimetype="application/json"
                )
            elif resultado == CodigosRespuesta.ERROR_INTERNO:
                respuesta = Response(status=CodigosRespuesta.ERROR_INTERNO)
            elif resultado == CodigosRespuesta.CONFLICTO:
                respuesta = Response(status=CodigosRespuesta.CONFLICTO)

    else:
        respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)

    return respuesta


@rutas_miembro.route("/miembros/<old_email>", methods=["PUT"])
def actualizar_miembro(old_email):
    valores_requeridos = {"email", "nickname", "contrasenia"}
    miembro_recibido = request.json
    respuesta = Response(CodigosRespuesta.MALA_SOLICITUD)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.email = miembro_recibido["email"]
        miembro.contrasenia = miembro_recibido["contrasenia"]
        miembro.nickname = miembro_recibido["nickname"]
        resultado = miembro.actualizar(old_email)
        if resultado == CodigosRespuesta.OK:
            respuesta = Response(
                json.dumps(miembro.convertir_a_json(["idMiembro", "email", "contrasenia", "nickname",
                                                         "estado", "tipoMiembros"])),
                status=CodigosRespuesta.OK,
                mimetype="application/json"
            )
        elif resultado == CodigosRespuesta.ERROR_INTERNO:
            respuesta = Response(status=CodigosRespuesta.ERROR_INTERNO)
        elif resultado == CodigosRespuesta.CONFLICTO:
            respuesta = Response(status= CodigosRespuesta.CONFLICTO)

    else:
        respuesta = Response(status=400)
    return respuesta


@rutas_miembro.route("/miembros", methods=["GET"])
def getprueba():
    respuesta = Response(
        json.dumps({
            "idMiembro": "Efrain",
            "email": "Razziel",
            "contrasenia": "Arenas",
            "nickname": "Ramirez",
            "estado": "Sexto",
            "tipoMiembro": "Semestre234"
        }),
        status=200,
        mimetype="application/json"
    )
    return respuesta


@rutas_miembro.route("/login", methods=["POST"])
def iniciar_sesion():
    valores_requeridos = {"email", "contrasenia"}
    miembro_recibido = request.json
    respuesta = Response(200)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.email = miembro_recibido["email"]
        miembro.contrasenia = miembro_recibido["contrasenia"]
        resultado = miembro.iniciar_sesion()
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
            respuesta = Response(status=404)
        elif resultado == 2:
            respuesta = Response(status=500)
        elif resultado == 3:
            respuesta = Response(status=404)
    else:
        respuesta = Response(status=400)
    return respuesta
