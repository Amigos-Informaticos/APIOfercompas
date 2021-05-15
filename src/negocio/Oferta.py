from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from src.negocio.Publicacion import Publicacion

Base = declarative_base()


class Oferta(Publicacion):
    __tablename__ = "Oferta"

    idPublicacion: Column = Column(Integer(), primary_key=True, nullable=False)
    precio: Column = Column(Float(), nullable=False, unique=False)
    vinculo: Column = Column(String(2048))

    def __init__(self):
        super().__init__()
        self.idPublicacion = None
        self.precio = None
        self.vinculo = None



