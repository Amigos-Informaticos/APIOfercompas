from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion


class CodigoDescuento(Publicacion):

    def __init__(self):
        super().__init__()
        self.codigo = None
        self.tipoPublicacion = "CodigoDescuento"

    def convertir_a_json(self, atributos: list)->dict:
        diccionario = {}
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key]=self.__getattribute__(key)
        return diccionario

    def registrar_codigo(self) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPI_registrarCodigoDescuento (%s, %s, %s, %s, %s, %s, %s)"
        values = [self.titulo, self.descripcion, self.fechaCreacion, self.fechaFin, self.categoria,
                  self.codigo, self.publicador]
        if conexion.send_query(query, values):
            respuesta = 201
        else:
            respuesta = 400

        return respuesta



    def actualizar_codigo(self, id_publicacin: int) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPA_actualizarCodigoDescuento(%s, %s, %s, %s, %s, %s, %s)"
        values = [id_publicacin, self.titulo, self.descripcion, self.fechaCreacion,
                  self.fechaFin, self.categoria, self.codigo]
        if conexion.send_query(query, values):
            respuesta = 200
        else:
            respuesta = 400

        return respuesta