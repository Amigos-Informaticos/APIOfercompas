from sqlalchemy import Column, String, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.datos.Conexion import Conexion
from src.negocio.EstadoMiembro import EstadoMiembro
from src.negocio.TipoMiembro import TipoMiembro

Base = declarative_base()


class MiembroOfercompas(Base, Conexion):
    __tablename__ = "MiembroOfercompas"

    idMiembro: Column = Column(Integer(), primary_key=True, nullable=False)
    nickname: Column = Column(String(20), nullable=False, unique=True)
    email: Column = Column(String(320), nullable=False, unique=True)
    contrasenia: Column = Column(String(20), nullable=False)

    def __init__(self, id_miembro: int = None, nickname: str = None, email: str = None, contrasenia: str = None,
                 estado: EstadoMiembro = 1, tipo_miembro: TipoMiembro = 1):
        self.idMiembro = id_miembro
        self.nickname = nickname
        self.email = email
        self.contrasenia = contrasenia
        self.estado = estado
        self.tipoMiembro = tipo_miembro

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
        self.email = miembro.email
        self.idMiembro = miembro.idMiembro
        self.contrasenia = miembro.contrasenia
        self.nickname = miembro.nickname

    def actualizar_miembro(self, old_email: str):
        actualizado = 1
        try:
            conexion: Session = MiembroOfercompas.abrir_conexion()
            miembro: MiembroOfercompas = conexion.query(MiembroOfercompas).filter_by(email=old_email).first()
            if miembro is not None:
                miembro.nickname = self.nickname
                miembro.contrasenia = self.contrasenia
                miembro.email = self.email
                self.idMiembro = miembro.idMiembro
                conexion.commit()
                actualizado = 0
            else:
                actualizado = 3 # miembro no existe en bd
        except SQLAlchemyError as sql_error:
            actualizado = 2
            print(sql_error)

        return actualizado