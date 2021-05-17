import json

from flask import Blueprint, request, Response

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, OK
from src.negocio.Oferta import Oferta
from src.servicios.Auth import Auth

rutas_oferta = Blueprint("rutas_oferta", __name__)


@rutas_oferta.route("/ofertas", methods=["POST"])
def registrar_oferta():
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "publicador", "categoria", "vinculo"}
    print(oferta_recibida)
    respuesta = Response(status=MALA_SOLICITUD)
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
            if status == RECURSO_CREADO:
                respuesta = Response(
                    json.dumps({
                        "idPublicacion": oferta.idPublicacion,
                        "titulo": oferta.titulo,
                        "descripcion": oferta.descripcion,
                        "fechaCreacion": oferta.fechaCreacion,
                        "fechaFin": oferta.fechaFin,
                        "publicador": oferta.publicador
                    }),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

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
