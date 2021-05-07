import json

from flask import Blueprint, request, Response

from src.model.MiembroOfercompas import MiembroOfercompas

rutas_miembro = Blueprint("rutas_miembro", __name__)


@rutas_miembro.route("/miembros", methods=["POST"])
def registrar_miembro():
	miembro_recibido = request.json
	valores_requeridos = {"email", "nickname", "contrasenia"}
	respuesta = Response(status=400)
	if all(llave in miembro_recibido for llave in valores_requeridos):
		miembro = MiembroOfercompas()
		miembro.email = miembro_recibido["email"]
		miembro.contrasenia = miembro_recibido["contrasenia"]
		miembro.nickname = miembro_recibido["nickname"]
		resultado = miembro.registrar()
		if resultado == 0:
			respuesta = Response(
				json.dumps({
					"idMiembro": miembro.idMiembro,
					"email": miembro.email,
					"contrasenia": miembro.contrasenia,
					"nickname": miembro.nickname,
					"estaActivo": miembro.estaActivo,
					"esModerador": miembro.esModerador
				}),
				status=201,
				mimetype="application/json"
			)
		elif resultado == 1:
			respuesta = Response(status=409)
		elif resultado == 2:
			respuesta = Response(status=500)
	return respuesta
