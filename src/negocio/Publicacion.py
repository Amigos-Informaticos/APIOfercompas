from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection
from src.negocio.EstadoPublicacion import EstadoPublicacion
from src.negocio.Puntuacion import Puntuacion
from src.transferencia_archivos.ServidorArchivos import ServidorArchivos


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
            respuesta = 200
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

    @staticmethod
    def obtener_publicaciones_denunciadas(pagina: int):
        conexion = EasyConnection()
        query = "CALL SPS_obtenerOfertasDenunciadas(%s)"
        values = [pagina]
        ofertas_obtenidas = conexion.select(query, values)
        resultado = []
        if ofertas_obtenidas:
            for oferta_individual in ofertas_obtenidas:
                oferta_aux = Publicacion()
                oferta_aux.idPublicacion = oferta_individual["idPublicacion"]
                oferta_aux.titulo = oferta_individual["titulo"]
                oferta_aux.descripcion = oferta_individual["descripcion"]
                oferta_aux.fechaCreacion = str(oferta_individual["fechaCreacion"])
                oferta_aux.fechaFin = str(oferta_individual["fechaFin"])
                oferta_aux.precio = oferta_individual["precio"]
                oferta_aux.vinculo = oferta_individual["vinculo"]
                oferta_aux.obtener_puntuacion()
                resultado.append(oferta_aux)
        return resultado

    def registrar_imagen(self, ruta: str) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "INSERT INTO Multimedia(ruta, idOferta, tipo) VALUES (%s, %s, 'foto');"
        values = [ruta, self.idPublicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado

    def registrar_video(self, ruta: str) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "INSERT INTO Multimedia(ruta, idOferta, tipo) VALUES (%s, %s, 'video');"
        values = [ruta, self.idPublicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado

    def obtener_ruta_foto_id(self) -> str:
        conexion = EasyConnection()
        query = "SELECT ruta FROM Multimedia WHERE idOferta = %s AND tipo = 'foto'"
        values = [self.idPublicacion]
        ruta = conexion.select(query, values)
        ruta_retorno = "not"
        if len(ruta) > 0:
            ruta_retorno = ruta[0]["ruta"]
        return ruta_retorno

    def obtener_ruta_video_id(self) -> str:
        conexion = EasyConnection()
        query = "SELECT ruta FROM Multimedia WHERE idOferta = %s AND tipo = 'video'"
        values = [self.idPublicacion]
        ruta = conexion.select(query, values)
        ruta_retorno = "not"
        if len(ruta) > 0:
            ruta_retorno = ruta[0]["ruta"]
        return ruta_retorno

    def recuperar_archivo(self, ruta_archivo):
        servidor = ServidorArchivos()
        resultado = servidor.obtener_archivos(ruta_archivo)
        imagen = resultado[0]
        return imagen

    def recuperar_imagenes_pagina(self, lista_ids):
        servidor = ServidorArchivos()
        imagenes = []
        for id in lista_ids:
            publicacion_aux = Publicacion()
            publicacion_aux.idPublicacion = id
            imagenes.append(publicacion_aux.recuperar_archivo())
        return imagenes

    def contar_imagenes(self):
        conexion = EasyConnection()
        query = "SELECT COUNT(id_imagen) AS CONTEO FROM Multimedia WHERE idOferta = %s;"
        values = [self.idPublicacion]
        resultado = conexion.select(query, values)
        return resultado[0]["CONTEO"]
