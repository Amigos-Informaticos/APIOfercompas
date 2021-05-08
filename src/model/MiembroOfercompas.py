from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, relationship

from src.model.Conexion import Conexion


class MiembroOfercompas(Conexion):
	__tablename__ = "Miembro"

	idMiembro: Column = Column(Integer(), primary_key=True, nullable=False)
	nickname: Column = Column(String(20), nullable=False, unique=True)
	email: Column = Column(String(320), nullable=False, unique=True)
	contrasenia: Column = Column(String(20), nullable=False)
	estaActivo: Column = Column(Boolean(), nullable=False, default=True)
	esModerador: Column = Column(Boolean(), nullable=False, default=False)
	referenciaPublicaciones = relationship("Publicacion", back_populates="referencia")

	def __init__(self, id_miembro: int = None, nickname: str = None, email: str = None, contrasenia: str = None,
				 esta_activo: bool = True,
				 es_moderador: bool = False):
		self.idMiembro = id_miembro
		self.nickname = nickname
		self.email = email
		self.contrasenia = contrasenia
		self.estaActivo = esta_activo
		self.esModerador = es_moderador

	def registrar(self) -> int:
		registrado = 1
		if not self.email_registrado() and not self.nickname_registrado():
			try:
				conexion: Session = MiembroOfercompas.abrir_conexion()
				conexion.add(self)
				conexion.commit()
				registrado = 0
				self.recuperar_miembro()
			except SQLAlchemyError as sql_error:
				registrado = 2
				print(sql_error)
		return registrado

	def iniciar_sesion(self) -> int:
		iniciado = 1
		if self.email_registrado():
			try:
				conexion: Session = MiembroOfercompas.abrir_conexion()
				miembro: MiembroOfercompas = conexion.query(MiembroOfercompas).filter_by(email=self.email).first()
				if miembro.contrasenia == self.contrasenia:
					iniciado = 0
			except SQLAlchemyError:
				iniciado = 2
		return iniciado

	def email_registrado(self) -> bool:
		conexion: Session = MiembroOfercompas.abrir_conexion()
		email_disponible: bool = conexion.query(
			conexion.query(MiembroOfercompas).filter_by(email=self.email).exists()
		).scalar()
		conexion.close()
		return email_disponible

	def nickname_registrado(self) -> bool:
		conexion: Session = MiembroOfercompas.abrir_conexion()
		nickname_disponible: bool = conexion.query(
			conexion.query(MiembroOfercompas).filter_by(nickname=self.nickname).exists()
		).scalar()
		conexion.close()
		return nickname_disponible

	def recuperar_miembro(self):
		conexion: Session = MiembroOfercompas.abrir_conexion()
		miembro: MiembroOfercompas = conexion.query(MiembroOfercompas).filter_by(email=self.email).first()
		self = miembro
