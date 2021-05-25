import json
from http import HTTPStatus

from flask import Blueprint, request, Response, jsonify

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, OK, NO_ENCONTRADO
from src.negocio.Oferta import Oferta
from src.servicios.Auth import Auth

rutas_oferta = Blueprint("rutas_oferta", __name__)


@rutas_oferta.route("/ofertas", methods=["POST"])
def registrar_oferta():
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "publicador", "categoria",
                          "vinculo"}
    print(oferta_recibida)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            oferta = Oferta()
            oferta.titulo = oferta_recibida["titulo"]
            oferta.descripcion = oferta_recibida["descripcion"]
            oferta.fechaCreacion = oferta_recibida["fechaCreacion"]
            oferta.fechaFin = oferta_recibida["fechaFin"]
            oferta.categoria = oferta_recibida["categoria"]
            oferta.publicador = oferta_recibida["publicador"]
            oferta.precio = oferta_recibida["precio"]
            oferta.vinculo = oferta_recibida["vinculo"]
            status = oferta.registrar_oferta()
            if status == HTTPStatus.OK:
                respuesta = Response(
                    oferta.convertir_a_json(),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=HTTPStatus.BAD_REQUEST)

    return respuesta


@rutas_oferta.route("/ofertas/<idPublicacion>", methods=["PUT"])
def actualizar_oferta(idPublicacion):
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "categoria", "vinculo"}
    respuesta = Response(status=MALA_SOLICITUD)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            oferta = Oferta()
            oferta.titulo = oferta_recibida["titulo"]
            oferta.descripcion = oferta_recibida["descripcion"]
            oferta.fechaCreacion = oferta_recibida["fechaCreacion"]
            oferta.fechaFin = oferta_recibida["fechaFin"]
            oferta.categoria = oferta_recibida["categoria"]
            oferta.precio = oferta_recibida["precio"]
            oferta.vinculo = oferta_recibida["vinculo"]
            status = oferta.actualizar_oferta(idPublicacion)
            if status == RECURSO_CREADO:
                respuesta = Response(
                    json.dumps(oferta.convertir_a_json(
                        ["idPublicacion", "titulo", "descripcion", "precio", "fechaCreacion", "fechaFin",
                         "categoria", "vinculo"])),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

    return respuesta


@rutas_oferta.route("/ofertas/<idPublicacion>", methods=["DELETE"])
def eliminar_oferta(idPublicacion):
    status = Oferta.eliminar_oferta(idPublicacion)
    return Response(status=status)


@rutas_oferta.route("/ofertas", methods=["GET"])
def obtener_oferta():
    pagina = request.args.get("pagina", default=1, type=int)
    categoria = request.args.get("categoria", default=-1, type=int)
    ofertas = Oferta.obtener_oferta(pagina, categoria)
    if ofertas:
        ofertas_jsons = []
        for oferta in ofertas:
            ofertas_jsons.append(oferta.convertir_a_json())
        prueba = json.dumps(ofertas_jsons)
        print(prueba)
        respuesta = Response(json.dumps(ofertas_jsons),status=OK,mimetype="application/json")
    else:
        respuesta = Response(status=NO_ENCONTRADO)
    return respuesta
