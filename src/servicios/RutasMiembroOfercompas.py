import json

from flask import Blueprint, request, Response, session

from src.negocio import CodigosRespuesta, TipoMiembro
from src.negocio.MiembroOfercompas import MiembroOfercompas
from src.servicios.Auth import Auth

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
@Auth.requires_token
@Auth.requires_role(TipoMiembro.COMUN)
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
            respuesta = Response(status=CodigosRespuesta.CONFLICTO)

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
    respuesta = Response(CodigosRespuesta.MALA_SOLICITUD)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.email = miembro_recibido["email"]
        miembro.contrasenia = miembro_recibido["contrasenia"]

        resultado = miembro.iniciar_sesion()
        if resultado == CodigosRespuesta.OK:
            token = Auth.generate_token(miembro)
            session.permanent = True
            session["token"] = token
            miembro_json = miembro.convertir_a_json(["idMiembro", "email", "contrasenia", "nickname",
                                                     "estado", "tipoMiembros"])
            miembro_json["token"] = token
            respuesta = Response(
                json.dumps(miembro_json),
                status=CodigosRespuesta.OK,
                mimetype="application/json"

            )
        else:
            respuesta = Response(status=resultado)
    else:
        respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)
    return respuesta
