import json

from flask import Blueprint, request, Response

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, NO_ENCONTRADO
from src.negocio.MiembroOfercompas import MiembroOfercompas
from src.negocio.Oferta import Oferta
from src.negocio.Publicacion import Publicacion

rutas_oferta = Blueprint("rutas_oferta", __name__)


@rutas_oferta.route("/ofertas", methods=["POST"])
def registrar_oferta():
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "publicador", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            miembro = MiembroOfercompas.obtener_con_id(oferta_recibida["publicador"])
            publicacion = Publicacion()
            publicacion.titulo = oferta_recibida["titulo"]
            publicacion.descripcion = oferta_recibida["descripcion"]
            publicacion.fechaCreacion = oferta_recibida["fechaCreacion"]
            publicacion.fechaFin = oferta_recibida["fechaFin"]
            publicacion.categoria = oferta_recibida["categoria"]
            publicacion.publicador = oferta_recibida["publicador"]
            publicacion.autor = miembro
            publicacion.__mapper_args__["polymorphic_identity"] = "Oferta"
            id_publicacion = publicacion.registrar_publicacion()
            print(id_publicacion)
            if miembro is not None and id_publicacion is not None:
                oferta = Oferta()
                oferta.precio = oferta_recibida["precio"]
                status = oferta.registrar_oferta(id_publicacion)
                if status == RECURSO_CREADO:
                    respuesta = Response(
                        json.dumps({
                            "idPublicacion": publicacion.idPublicacion,
                            "titulo": publicacion.titulo,
                            "descripcion": publicacion.descripcion,
                            "fechaCreacion": publicacion.fechaCreacion,
                            "fechaFin": publicacion.fechaFin,
                            "publicador": publicacion.publicador
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
