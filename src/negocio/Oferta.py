from http import HTTPStatus

from flask import json

from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion


class Oferta(Publicacion):

    def __init__(self):
        super().__init__()
        self.precio = None
        self.vinculo = None
        self.tipoPublicacion = "Oferta"

    def hacer_json(self):
        return json.dumps({"titulo": self.titulo,
                           "descripcion": self.descripcion,
                           "precio": self.precio,
                           "fechaCreacion": self.fechaCreacion})

    def convertir_a_json(self, atributos: list) -> dict:
        diccionario = {}
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def registrar_oferta(self) -> int:
        respuesta = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "CALL SPI_registrarOferta (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [self.titulo, self.descripcion, self.precio, self.fechaCreacion, self.fechaFin, self.categoria,
                  self.vinculo, self.publicador]
        print(values)
        if conexion.send_query(query, values):
            respuesta = HTTPStatus.CREATED
        else:
            respuesta = HTTPStatus.BAD_REQUEST

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

    @staticmethod
    def obtener_oferta(pagina: int, categoria: int):
        conexion = EasyConnection()
        query = "CALL SPS_obtenerOfertasGeneral(%s, %s)"
        values = [pagina, categoria]
        ofertas_obtenidas = conexion.select(query, values)
        resultado = []
        if ofertas_obtenidas:
            for oferta_individual in ofertas_obtenidas:
                oferta_aux = Oferta()
                oferta_aux.idPublicacion = oferta_individual["idPublicacion"]
                oferta_aux.titulo = oferta_individual["titulo"]
                oferta_aux.descripcion = oferta_individual["descripcion"]
                oferta_aux.fechaCreacion = str(oferta_individual["fechaCreacion"])
                oferta_aux.fechaFin = str(oferta_individual["fechaFin"])
                oferta_aux.precio = oferta_individual["precio"]
                oferta_aux.vinculo = oferta_individual["vinculo"]
                resultado.append(oferta_aux)
        return resultado
