from sqlalchemy.exc import SQLAlchemyError

from src.datos.EasyConnection import EasyConnection
from src.negocio.EstadoPublicacion import EstadoPublicacion


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

    def estaRegistrada(self) -> bool:
        pass

    def registrar_publicacion(self) -> int:
        pass

    def obtener_por_autoria(self) -> int:
        pass

    def obtener_id(self) -> int:
        id = None
        conexion = EasyConnection()
        query = "SELECT idPublicacion FROM Publicacion WHERE titulo = %s AND descripcion = %s AND publicador = %s;"
        values = [self.titulo, self.descripcion, self.publicador]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            id = resultado[0][0]
        return id
