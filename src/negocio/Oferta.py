from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion


class Oferta(Publicacion):

    def __init__(self):
        super().__init__()
        self.precio = None
        self.vinculo = None
        self.tipoPublicacion = "Oferta"

    def convertir_a_json(self, atributos: list) -> dict:
        diccionario = {}
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def registrar_oferta(self) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPI_registrarOferta (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [self.titulo, self.descripcion, self.precio, self.fechaCreacion, self.fechaFin, self.categoria,
                  self.vinculo, self.publicador]
        print(values)
        if conexion.send_query(query, values):
            respuesta = 201
        else:
            respuesta = 400

        return respuesta

    def actualizar_oferta(self, id_publicacin: int) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPA_actualizarOferta(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [id_publicacin, self.titulo, self.descripcion, self.precio, self.fechaCreacion,
                  self.fechaFin, self.categoria, self.vinculo]
        if conexion.send_query(query, values):
            respuesta = 200
        else:
            respuesta = 400

        return respuesta

