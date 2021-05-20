from src.datos.EasyConnection import EasyConnection
from src.negocio import CodigosRespuesta, EstadoMiembro, TipoMiembro


class MiembroOfercompas():
    def __init__(self):
        self.idMiembro = None
        self.nickname = None
        self.email = None
        self.contrasenia = None
        self.estado = EstadoMiembro.ACTIVO
        self.tipoMiembro = TipoMiembro.COMUN

    def convertir_a_json(self, atributos: list) -> dict:
        diccionario = {}
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def email_registrado(self) -> bool:
        status = False
        conexion = EasyConnection()
        query = "SELECT * FROM MiembroOfercompas WHERE email = %s;"
        values = [self.email]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status

    def nickname_registrado(self) -> bool:
        status = False
        conexion = EasyConnection()
        query = "SELECT * FROM MiembroOfercompas WHERE nickname = %s;"
        values = [self.nickname]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status

    def registrar(self) -> int:
        registrado = CodigosRespuesta.ERROR_INTERNO
        if not self.email_registrado() and not self.nickname_registrado():
            query = "INSERT INTO MiembroOfercompas(email, contrasenia, estado, tipoMiembro, nickname) VALUES " \
                    "(%s, %s, %s, %s, %s) ;"
            values = [self.email, self.contrasenia, self.estado, self.tipoMiembro, self.nickname]
            conexion = EasyConnection()
            conexion.send_query(query, values)
            self.idMiembro = self.getId()
            registrado = CodigosRespuesta.RECURSO_CREADO
        else:
            registrado = CodigosRespuesta.CONFLICTO
        return registrado

    def actualizar(self, old_email: str):
        actualizado = CodigosRespuesta.ERROR_INTERNO
        if not self.email_registrado_actualizar():
            query = "UPDATE MiembroOfercompas SET nickname = %s, email = %s, contrasenia = %s WHERE email = %s"
            values = [self.nickname, self.email, self.contrasenia, old_email]
            conexion = EasyConnection()
            conexion.send_query(query, values)
            actualizado = CodigosRespuesta.OK
        else:
            actualizado = CodigosRespuesta.CONFLICTO
        return actualizado

    def getId(self) -> int:
        id_recuperado = -1
        query = "SELECT idMiembro FROM MiembroOfercompas WHERE email = %s;"
        values = [self.email]
        conexion = EasyConnection()
        resultados = conexion.select(query, values)
        id_recuperado = resultados[0]["idMiembro"]
        return id_recuperado

    def email_registrado_actualizar(self) -> bool:
        status = False
        conexion = EasyConnection()
        self.idMiembro = self.getId()
        query = "SELECT * FROM MiembroOfercompas WHERE email = %s AND idMiembro <> %s;"
        values = [self.email, self.idMiembro]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status
