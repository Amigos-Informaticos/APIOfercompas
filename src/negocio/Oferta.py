from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.negocio.Publicacion import Publicacion

Base = declarative_base()


class Oferta(Publicacion):
    __tablename__ = "Oferta"

    idPublicacion: Column = Column(Integer(), primary_key=True, nullable=False)
    precio: Column = Column(Float(), nullable=False, unique=False)
    vinculo: Column = Column(String(2048))

    def __init__(self):
        super().__init__()
        self.precio = None
        self.vinculo = None

    def registrar(self) -> int:
        registrado = 409
        if not self.estaRegistrada():
            try:
                conexion: Session = Oferta.abrir_conexion()
                conexion.add(self)
                conexion.commit()
                registrado = 201
                self.recuperar_miembro()
            except SQLAlchemyError as sql_error:
                registrado = 500
                print(sql_error)
        return registrado
