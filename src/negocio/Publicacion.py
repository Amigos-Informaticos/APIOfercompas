from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

from src.negocio.Categoria import Categoria
from src.datos.Conexion import Conexion
from src.negocio.EstadoPublicacion import EstadoPublicacion


class Publicacion(Conexion):
    __tablename__ = "Publicacion"

    idPublicacion: Column = Column(Integer(), primary_key=True, nullable=False)
    titulo: Column = Column(String(200), nullable=False)
    descripcion: Column = Column(String(500), nullable=False)
    estado: Column = Column(Integer(), nullable=False, default=1)
    fechaCreacion: Column = Column(Date(), nullable=False)
    fechaFin: Column = Column(Date(), nullable=False)
    categoria: Column = Column(Integer(), ForeignKey("Categoria.idCategoria"), nullable=False)
    publicador: Column = Column(Integer(), ForeignKey("MiembroOfercompas.idMiembro"), nullable=False)
    tipoPublicacion: Column = Column(String(10), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "Publicacion",
        "polymorphic_on": tipoPublicacion}

    def __init__(self):
        self.idPublicacion = 0
        self.titulo = None
        self.descripcion = None
        self.estado = EstadoPublicacion.ACTIVA.value
        self.fechaCreacion = None
        self.fechaCreacion = None
        self.publicador = None
        self.categoria = 1
        self.conexion = Publicacion.abrir_conexion()

    def estaRegistrada(self) -> bool:
        repetido: bool = self.conexion.query(
            self.conexion.query(Publicacion).filter_by(titulo=self.titulo, descripcion=self.descripcion).exists()
        ).scalar()
        self.conexion.close()
        return repetido

    def registrar_publicacion(self, tipo_publicacion: str) -> int:
        id = None
        self.tipoPublicacion = tipo_publicacion
        if not self.estaRegistrada():
            try:
                self.conexion.add(self)
                self.conexion.commit()
                print(self.idPublicacion)
                id = self.idPublicacion
            except SQLAlchemyError as sql_error:
                print(sql_error)
            finally:
                self.conexion.close()
        return id
