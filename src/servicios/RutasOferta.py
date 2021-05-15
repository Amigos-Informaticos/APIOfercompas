import json

from flask import Blueprint, request, Response

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, NO_ENCONTRADO
from src.negocio.MiembroOfercompas import MiembroOfercompas
from src.negocio.Oferta import Oferta

rutas_oferta = Blueprint("rutas_oferta", __name__)


@rutas_oferta.route("/ofertas", methods=["POST"])
def registrar_oferta():
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "publicador", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            miembro = MiembroOfercompas.obtener_con_id(oferta_recibida["publicador"])
            if miembro is not None:
                oferta = Oferta()
                oferta.titulo = oferta_recibida["titulo"]
                oferta.descripcion = oferta_recibida["descripcion"]
                oferta.precio = oferta_recibida["precio"]
                oferta.fechaCreacion = oferta_recibida["fechaCreacion"]
                oferta.fechaFin = oferta_recibida["fechaFin"]
                oferta.categoria = oferta_recibida["categoria"]
                oferta.publicador = oferta_recibida["publicador"]
                oferta.autor = miembro
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
                respuesta = Response(status=NO_ENCONTRADO)
    else:
        respuesta = Response(status=MALA_SOLICITUD)

    return respuesta