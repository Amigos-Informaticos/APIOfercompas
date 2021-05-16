from sqlalchemy import Column, String, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from src.datos.Conexion import Conexion
from src.negocio.EstadoMiembro import EstadoMiembro
from src.negocio.TipoMiembro import TipoMiembro

Base = declarative_base()


class MiembroOfercompas(Conexion):
    __tablename__ = "MiembroOfercompas"

    idMiembro: Column = Column(Integer(), primary_key=True, nullable=False)
    nickname: Column = Column(String(20), nullable=False, unique=True)
    email: Column = Column(String(320), nullable=False, unique=True)
    contrasenia: Column = Column(String(20), nullable=False)
    estado: Column = Column(Integer(), nullable=False, unique=False)
    tipoMiembro: Column = Column(Integer(), nullable=False, unique=False)
    referenciaPublicaciones = relationship("Publicacion", backref="autor")

    def __init__(self, id_miembro: int = None, nickname: str = None, email: str = None, contrasenia: str = None,
                 estado: EstadoMiembro = 1, tipo_miembro: TipoMiembro = 1):
        self.idMiembro = id_miembro
        self.nickname = nickname
        self.email = email
        self.contrasenia = contrasenia
        self.estado = estado
        self.tipoMiembro = tipo_miembro
        self.conexion = MiembroOfercompas.abrir_conexion()

    def registrar(self) -> int:
        registrado = 1
        if not self.email_registrado() and not self.nickname_registrado():
            try:
                self.self.conexion.add(self)
                self.self.conexion.commit()
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
                miembro: MiembroOfercompas = self.conexion.query(MiembroOfercompas).filter_by(email=self.email).first()
                if miembro.contrasenia == self.contrasenia:
                    iniciado = 0
            except SQLAlchemyError:
                iniciado = 2
        return iniciado

    def email_registrado(self) -> bool:
        email_disponible: bool = self.conexion.query(
            self.conexion.query(MiembroOfercompas).filter_by(email=self.email).exists()
        ).scalar()
        self.conexion.close()
        return email_disponible

    def nickname_registrado(self) -> bool:
        nickname_disponible: bool = self.conexion.query(
            self.conexion.query(MiembroOfercompas).filter_by(nickname=self.nickname).exists()
        ).scalar()
        self.conexion.close()
        return nickname_disponible

    def recuperar_miembro(self):
        miembro: MiembroOfercompas = self.conexion.query(MiembroOfercompas).filter_by(email=self.email).first()
        self.email = miembro.email
        self.idMiembro = miembro.idMiembro
        self.contrasenia = miembro.contrasenia
        self.nickname = miembro.nickname

    def actualizar_miembro(self, old_email: str):
        actualizado = 1
        try:
            miembro: MiembroOfercompas = self.conexion.query(MiembroOfercompas).filter_by(email=old_email).first()
            if miembro is not None:
                miembro.nickname = self.nickname
                miembro.contrasenia = self.contrasenia
                miembro.email = self.email
                self.idMiembro = miembro.idMiembro
                self.conexion.commit()
                actualizado = 0
            else:
                actualizado = 3  # miembro no existe en bd
        except SQLAlchemyError as sql_error:
            actualizado = 2
            print(sql_error)

        return actualizado

    def eliminar_miembro(self, id_miembro: int):
        eliminado = 1
        try:
            miembro: MiembroOfercompas = self.conexion.query(MiembroOfercompas).filter_by(id=id_miembro).first()
            if miembro is not None:
                miembro.estado = 3
                eliminado = 0
                self.conexion.commit()
            else:
                eliminado = 3
        except SQLAlchemyError as sql_error:
            eliminado = 2
            print(sql_error)

        return eliminado

    def expulsar_miembro(self, id_miembro: int):
        expulsado = 1
        try:
            miembro: MiembroOfercompas = self.conexion.query(MiembroOfercompas).filter_by(id=id_miembro).first()
            if miembro is not None:
                miembro.estado = 2
                expulsado = 0
                self.conexion.commit()
            else:
                expulsado = 3
        except SQLAlchemyError as sql_error:
            expulsado = 2
            print(sql_error)

        return expulsado

    @staticmethod
    def obtener_con_id(id_miembro: int):
        miembro = None
        try:
            conexion: Session = MiembroOfercompas.abrir_conexion()
            miembro: MiembroOfercompas = conexion.query(MiembroOfercompas).filter_by(idMiembro=id_miembro).first()
            conexion.expunge_all()
            conexion.close()
        except SQLAlchemyError as sql_error:
            print(sql_error)

        return miembro




