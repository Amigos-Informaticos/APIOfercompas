from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from src.negocio.Publicacion import Publicacion

Base = declarative_base()


class Oferta(Publicacion):
    __tablename__ = "Oferta"

    idPublicacion: Column = Column(Integer(), ForeignKey("Publicacion.idPublicacion"), primary_key=True, nullable=False)
    precio: Column = Column(Float(), nullable=False, unique=False)
    vinculo: Column = Column(String(2048))
    __mapper_args__ = {"polymorphic_identity": "Oferta"}

    def __init__(self):
        super().__init__()
        self.precio = None
        self.vinculo = None

    def registrar_oferta(self) -> int:
        registrado = 409
        if not self.estaRegistrada():
            try:
                id_publicacion = self.registrar_publicacion("Oferta")
                if id_publicacion is not None:
                    self.idPublicacion = id_publicacion
                    self.conexion.add(self)
                    self.conexion.commit()
                    registrado = 201
                else:
                    registrado = 500
            except SQLAlchemyError as sql_error:
                registrado = 500
                print(sql_error)
            finally:
                self.conexion.close()
        return registrado
