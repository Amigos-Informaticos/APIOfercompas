import json

from flask import Blueprint, request, Response

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, OK
from src.negocio.CodigoDescuento import CodigoDescuento
from src.servicios.Auth import Auth

rutas_codigo = Blueprint("rutas_codigo", __name__)


@rutas_codigo.route("/codigos", methods=["POST"])
def registrar_codigo():
    codigo_recibido = request.json
    valores_requeridos = {"titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin", "publicador", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if codigo_recibido is not None:
        if all(llave in codigo_recibido for llave in valores_requeridos):
            codigo_descuento = CodigoDescuento()
            codigo_descuento.titulo = codigo_recibido["titulo"]
            codigo_descuento.descripcion = codigo_recibido["descripcion"]
            codigo_descuento.fechaCreacion = codigo_recibido["fechaCreacion"]
            codigo_descuento.fechaFin = codigo_recibido["fechaFin"]
            codigo_descuento.categoria = codigo_recibido["categoria"]
            codigo_descuento.publicador = codigo_recibido["publicador"]
            codigo_descuento.codigo = codigo_recibido["codigo"]
            status = codigo_descuento.registrar_codigo()
            if status == RECURSO_CREADO:
                respuesta = Response(
                    json.dumps({
                        "idPublicacion": codigo_descuento.idPublicacion,
                        "titulo": codigo_descuento.titulo,
                        "descripcion": codigo_descuento.descripcion,
                        "fechaCreacion": codigo_descuento.fechaCreacion,
                        "fechaFin": codigo_descuento.fechaFin,
                        "publicador": codigo_descuento.publicador,
                        "codigo": codigo_descuento.codigo
                    }),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

    return respuesta


@rutas_codigo.route("/codigos/<idPublicacion>", methods=["PUT"])
def actualizar_codigo(idPublicacion):
    codigo_recibido = request.json
    valores_requeridos = {"titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if codigo_recibido is not None:
        if all(llave in codigo_recibido for llave in valores_requeridos):
            codigo_descuento = CodigoDescuento()
            codigo_descuento.titulo = codigo_recibido["titulo"]
            codigo_descuento.descripcion = codigo_recibido["descripcion"]
            codigo_descuento.fechaCreacion = codigo_recibido["fechaCreacion"]
            codigo_descuento.fechaFin = codigo_recibido["fechaFin"]
            codigo_descuento.categoria = codigo_recibido["categoria"]
            codigo_descuento.codigo = codigo_recibido["codigo"]
            status = codigo_descuento.actualizar_codigo(idPublicacion)
            if status == RECURSO_CREADO:
                respuesta = Response(
                    json.dumps(codigo_descuento.convertir_a_json(
                        ["idPublicacion", "titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin",
                         "categoria"])),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

    return respuesta


@rutas_codigo.route("/codigos/<idPublicacion>", methods=["DELETE"])
def eliminar_codigo(idPublicacion):
    status = CodigoDescuento.eliminar_codigo(idPublicacion)
    return Response(status=status)
