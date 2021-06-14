import io
import json
from http import HTTPStatus

from flask import Blueprint, Response, request, send_file

from src.negocio.Oferta import Oferta
from src.negocio.Publicacion import Publicacion
from src.negocio.Puntuacion import Puntuacion
from src.servicios.Auth import Auth
from src.transferencia_archivos.ServidorArchivos import ServidorArchivos

rutas_publicacion = Blueprint("rutas_publicacion", __name__)


@rutas_publicacion.route("/publicaciones/<idPublicacion>", methods=["DELETE"])
def eliminar_publicacion(idPublicacion):
    status = Publicacion.eliminar_publicacion(idPublicacion)
    return Response(status=status)


@rutas_publicacion.route("/publicaciones/<idPublicacion>", methods=["GET"])
def obtener_interaccion(idPublicacion):
    parametros = request.headers
    if "idMiembro" in parametros:
        id_miembro = parametros.get("idMiembro")
        respuesta = Response(json.dumps(Publicacion.obtener_interaccion(id_miembro, idPublicacion)),
                             status=HTTPStatus.OK)
    else:
        respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta


@rutas_publicacion.route("/publicaciones/<idPublicacion>/puntuaciones", methods=["POST"])
def puntuar_publicacion(idPublicacion):
    puntuacion_recibida = request.json
    valores_requeridos = {"idMiembro", "esPositiva"}
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if puntuacion_recibida is not None:
        if all(llave in puntuacion_recibida for llave in valores_requeridos):
            puntuacion = Puntuacion()
            puntuacion.instanciar_con_hashmap(puntuacion_recibida, idPublicacion)
            resultado = puntuacion.puntuar_publicacion()
            if resultado == HTTPStatus.CREATED:
                respuesta = Response(puntuacion.convertir_a_json(),
                                     status=resultado,
                                     mimetype="application/json")
            else:
                respuesta = Response(status=resultado)
    return respuesta


@rutas_publicacion.route("/publicaciones/<idPublicacion>/imagenes", methods=["POST"])
def publicar_imagen(idPublicacion):
    print(request.files)
    imagen = request.files.getlist("imagen")[0]
    print("Archivo:"+ imagen.content_type)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)

    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    print(publicacion.idPublicacion)
    if imagen.content_type == "image/png":
        ruta = str(idPublicacion + "-" + imagen.filename + "-foto.png")
    else:
        ruta = str(idPublicacion + "-" + imagen.filename + "-video.mp4")
    servidor = ServidorArchivos()
    resultado = 0
    resultado = servidor.guardar_archivo(imagen, ruta)
    if resultado == 0:
        publicacion.registrar_imagen(ruta)

    respuesta = Response(status=HTTPStatus.CREATED)

    return respuesta


@rutas_publicacion.route("/publicaciones/<idPublicacion>/imagenes", methods=["GET"])
def recuperar_imagen(idPublicacion):
    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    resultado = publicacion.recuperar_imagen()
    response = Response(status=HTTPStatus.NOT_FOUND)
    if resultado:
        response = send_file(
            io.BytesIO(resultado),
            mimetype="image/png",
            as_attachment=False)
    return response

@rutas_publicacion.route("/publicaciones/<idPublicacion>/videos", methods=["GET"])
def recuperar_video(idPublicacion):
    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    resultado = publicacion.recuperar_imagen()
    response = Response(status=HTTPStatus.NOT_FOUND)
    if resultado:
        response = send_file(
            io.BytesIO(resultado),
            mimetype="video/mp4",
            as_attachment=False)
    return response

@rutas_publicacion.route("/publicaciones/imagenes", methods=["GET"])
def recuperar_imagenes_pagina():
    lista_ids = request.json
