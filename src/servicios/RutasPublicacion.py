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
    print(puntuacion_recibida)
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

@rutas_publicacion.route("/ofertas/<idPublicacion>/imagenes", methods=["POST"])
def publicar_imagen(idPublicacion):
    imagenes = []
    for imagen in request.files.getlist("imagenes"):
        imagenes.append(imagen)

    oferta = Oferta()
    oferta.idPublicacion = 28

    rutas = oferta.construir_rutas(len(imagenes))
    servidor = ServidorArchivos()
    resultado = 0
    indice = 0
    while indice < len(imagenes) and resultado == 0:
        resultado = servidor.guardar_archivo(imagenes[indice], rutas[indice])
        if resultado == 0:
            oferta.registrar_imagen(rutas[indice])
        indice += 1

    return Response(status=200)



