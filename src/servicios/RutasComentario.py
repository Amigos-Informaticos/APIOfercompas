import json
from http import HTTPStatus

from flask import Blueprint, request, Response, session

from src.negocio.Comentario import Comentario

rutas_comentario = Blueprint("rutas_comentario", __name__)


@rutas_comentario.route("/comentarios", methods=["POST"])
def registrar_comentario():
    comentario_recibido = request.json
    valores_requeridos = {"idPublicacion", "idMiembro", "contenido"}
    print(comentario_recibido)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if comentario_recibido is not None:
        if all(llave in comentario_recibido for llave in valores_requeridos):
            comentario = Comentario()
            comentario.instanciar_con_hashmap(comentario_recibido)
            resultado = comentario.registrar()
            if resultado == HTTPStatus.CREATED:
                respuesta = Response(comentario.hacer_json_sin_nickname(),
                                     status=resultado,
                                     mimetype="application/json")

            else:
                respuesta = Response(status=resultado)
    return respuesta


@rutas_comentario.route("/comentarios", methods=["GET"])
def obtener_comentarios():
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    id_publicacion = request.args.get("idPublicacion")

    if id_publicacion is not None:
        comentarios = Comentario.obtener_comentarios(id_publicacion)
        if comentarios:
            array_comentarios = []
            for comentario in comentarios:
                array_comentarios.append(comentario.hacer_json_nickname_contenido())
            comentarios_json = json.dumps(array_comentarios)
            print(comentarios_json)
            respuesta = Response(comentarios_json, status=HTTPStatus.OK, mimetype="application/json")
        else:
            respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta
