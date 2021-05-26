from http import HTTPStatus

from flask import Blueprint, request, Response, session

from src.negocio.Denuncia import Denuncia

rutas_denuncia = Blueprint("rutas_denuncia", __name__)


@rutas_denuncia.route("/denuncias", methods=["POST"])
def registrar_denuncia():
    denuncia_recibida = request.json
    valores_requeridos = {"idPublicacion", "idDenunciante", "comentario", "motivo"}
    print(denuncia_recibida)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if denuncia_recibida is not None:
        if all(llave in denuncia_recibida for llave in valores_requeridos):
            denuncia = Denuncia()
            denuncia.instanciar_con_hashmap(denuncia_recibida)
            resultado = denuncia.registrar()
            if resultado == HTTPStatus.CREATED:
                respuesta = Response(denuncia.hacer_json(),
                                     status=resultado,
                                     mimetype="application/json")

            else:
                respuesta = Response(status=resultado)
    return respuesta
