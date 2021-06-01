from src.datos.EasyConnection import EasyConnection
from src.negocio.EstadoPublicacion import EstadoPublicacion
from src.negocio.Puntuacion import Puntuacion


class Publicacion:

    def __init__(self):
        self.idPublicacion = 0
        self.titulo = None
        self.descripcion = None
        self.estado = EstadoPublicacion.ACTIVA.value
        self.fechaCreacion = None
        self.fechaFin = None
        self.publicador = None
        self.categoria = 1
        self.conexion = EasyConnection()
        self.puntuacion = 0

    def obtener_id(self) -> int:
        id = None
        conexion = EasyConnection()
        query = "SELECT idPublicacion FROM Publicacion WHERE titulo = %s AND descripcion = %s AND publicador = %s;"
        values = [self.titulo, self.descripcion, self.publicador]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            id = resultado[0][0]
        return id

    @staticmethod
    def eliminar_publicacion(id_publicacion: int) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPE_eliminarPublicacion(%s)"
        values = [id_publicacion]
        if conexion.send_query(query, values):
            respuesta = 204
        else:
            respuesta = 400

        return respuesta

    @staticmethod
    def obtener_interaccion(id_miembro: int, id_publicacion: int) -> dict:
        interacciones = {}
        interacciones["puntuada"] = Puntuacion.ha_puntuado(id_miembro, id_publicacion)
        interacciones["denunciada"] = Publicacion.ha_denunciado(id_miembro, id_publicacion)
        return interacciones

    @staticmethod
    def ha_denunciado(id_miembro: int, id_publicacion: int) -> bool:
        conexion = EasyConnection()
        query = "SELECT idMiembro FROM Denuncia WHERE idMiembro = %s AND idPublicacion = %s"
        values = [id_miembro, id_publicacion]
        resultado = conexion.select(query, values)
        return len(resultado) > 0

    def obtener_puntuacion(self):
        self.puntuacion = Puntuacion.calcular_puntuacion(self.idPublicacion)

