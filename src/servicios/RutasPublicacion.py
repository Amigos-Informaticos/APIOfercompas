from flask import Blueprint, Response

from src.negocio.Publicacion import Publicacion

rutas_publicacion = Blueprint("rutas_publicacion", __name__)


@rutas_publicacion.route("/publicaciones/<idPublicacion>", methods=["DELETE"])
def eliminar_publicacion(idPublicacion):
    status = Publicacion.eliminar_publicacion(idPublicacion)
    return Response(status=status)
