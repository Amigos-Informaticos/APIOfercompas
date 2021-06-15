import json
from http import HTTPStatus

from flask import Blueprint, Response, request

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


@rutas_publicacion.route("/publicaciones/<idPublicacion>/interaccion", methods=["GET"])
def obtener_interaccion(idPublicacion):
    print("OBTENIENDO INTERACCION")
    payload = request.json
    print(request)
    print(payload)
    valores_requeridos = ["idMiembro"]
    if payload is not None:
        if all(llave in payload for llave in valores_requeridos):
            id_miembro = payload.get("idMiembro")
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


@rutas_publicacion.route("/publicaciones/<idPublicacion>/multimedia", methods=["POST"])
def publicar_archivo(idPublicacion):
    print(request.files)
    archivo = request.files.getlist("imagen")[0]
    print("Archivo:" + archivo.content_type)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)

    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    print(publicacion.idPublicacion)
    servidor = ServidorArchivos()
    resultado = 0
    print("ARCHIVOOOO: "+archivo.content_type)
    if archivo.content_type == "image/png" or archivo.content_type == "image/jpeg":
        ruta = str(idPublicacion + "-" + archivo.filename)
        resultado = servidor.guardar_archivo(archivo, ruta)
        if resultado == 0:
            publicacion.registrar_imagen(ruta)
            respuesta = Response(status=HTTPStatus.CREATED)
    else:
        ruta = str(idPublicacion + "-" + archivo.filename)
        resultado = servidor.guardar_archivo(archivo, ruta)
        if resultado == 0:
            publicacion.registrar_video(ruta)
            respuesta = Response(status=HTTPStatus.CREATED)

    return respuesta


@rutas_publicacion.route("/publicaciones/<idPublicacion>/imagenes", methods=["GET"])
def recuperar_imagen(idPublicacion):
    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    response = Response(status=HTTPStatus.NOT_FOUND)
    ruta_foto = publicacion.obtener_ruta_foto_id()
    print("CACA:" + ruta_foto)
    if ruta_foto != "not":
        print("ENTRÓ!!!!!!!!")
        resultado = publicacion.recuperar_archivo(ruta_foto)
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
    response = Response(status=HTTPStatus.NOT_FOUND)
    ruta_video = publicacion.obtener_ruta_video_id()
    print("PIPI:" + ruta_video)
    if ruta_video != "not":
        print("VIDEO!!!!!!!!")
        resultado = publicacion.recuperar_archivo(ruta_video)
        if resultado:
            response = send_file(
                io.BytesIO(resultado),
                mimetype="video/mp4",
                as_attachment=False)

    return response


@rutas_publicacion.route("/publicaciones/imagenes", methods=["GET"])
def recuperar_imagenes_pagina():
    lista_ids = request.json
