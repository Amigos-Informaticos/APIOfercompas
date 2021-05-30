import json
from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection


class Denuncia():
    def __init__(self):
        self.id_publicacion = None
        self.id_denunciante = None
        self.comentario = None
        self.motivo = None

    def hacer_json(self):
        return json.dumps({"idPublicacion": self.id_publicacion,
                           "idDenunciante": self.id_denunciante,
                           "comentario": self.comentario,
                           "motivo": self.motivo
                           })

    def instanciar_con_hashmap(self, hash_denuncia: dict):
        self.id_publicacion = hash_denuncia["idPublicacion"]
        self.id_denunciante = hash_denuncia["idDenunciante"]
        self.comentario = hash_denuncia["comentario"]
        self.motivo = hash_denuncia["motivo"]

    def registrar(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.existe_publicacion() and self.existe_miembro():
            if not self.existe_denuncia():
                conexion = EasyConnection()
                query = "INSERT INTO Denuncia(idMiembro, idPublicacion, comentario, motivo) VALUES" \
                        "(%s,%s, %s, %s);"
                values = [self.id_denunciante, self.id_publicacion, self.comentario, self.motivo]
                conexion.send_query(query, values)
                status = HTTPStatus.CREATED
            else:
                status = HTTPStatus.CONFLICT
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    def existe_denuncia(self) -> bool:
        existe = False
        query = "SELECT * FROM Denuncia WHERE idPublicacion = %s and idMiembro = %s;"
        values = [self.id_publicacion, self.id_denunciante]
        conexion = EasyConnection()
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            existe = True

        return existe

    def existe_publicacion(self)->bool:
        existe = False
        query = "SELECT * FROM Publicacion WHERE idPublicacion = %s AND estado = 1;"
        values = [self.id_publicacion]
        conexion = EasyConnection()
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            existe = True

        return existe

    def existe_miembro(self)->bool:
        existe = False
        query = "SELECT * FROM MiembroOfercompas WHERE idMiembro = %s;"
        values = [self.id_denunciante]
        conexion = EasyConnection()
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            existe = True

        return existe