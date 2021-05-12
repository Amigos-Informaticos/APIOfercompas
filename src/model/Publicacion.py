from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Session

from src.model import EstadoPublicacion
from src.model.Conexion import Conexion


class Publicacion(Conexion):
	__tablename__ = "Publicacion"

	idPublicacion: Column = Column(Integer(), primary_key=True, nullable=False)
	titulo: Column = Column(String(200), nullable=False)
	descripcion: Column = Column(String(500), nullable=False)
	estado: Column = Column(Integer(), nullable=False, default=1)
	fechaCreacion: Column = Column(Date(), nullable=False)
	fechaFin: Column = Column(Date(), nullable=False)
	referencia = relationship("Miembro", back_populates="referenciaPublicaciones")
	publicador: Column(Integer(), ForeignKey("MiembroOfercompas.idMiembro"), nullable=False)


	def __init__(self):
		self.idPublicacion = 0
		self.titulo = None
		self.descripcion = None
		self.estado = EstadoPublicacion.ACTIVO
		self.fechaCreacion = None
		self.fechaCreacion = None
		self.publicador = None

	def estaRegistrada(self) -> bool:
		conexion: Session = Publicacion.abrir_conexion()
		repetido: bool = conexion.query(
			conexion.query(Publicacion).filter_by(titulo=self.titulo, descripcion=self.descripcion).exists()
		).scalar()
		conexion.close()
		return repetido

