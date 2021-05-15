from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from src.datos.Conexion import Conexion

Base = declarative_base()


class Publicacion(Conexion):
    __tablename__ = "Publicacion"

    idPublicacion: Column = Column(Integer(), primary_key=True, nullable=False)
    titulo: Column = Column(String(200), nullable=False, unique=False)
    descripcion: Column = Column(String(500), nullable=False, unique=False)
    estado: Column = Column(Integer(), nullable=False, unique=False)
    categoria: Column = Column(Integer(), nullable=False, unique=False)
    publicador: Column = Column(Integer(), nullable=False, unique=False)
    fechaCreacion: Column = Column(DateTime(), nullable=False, unique=False)
    fechaFin: Column = Column(DateTime(), nullable=False, unique=False)

    def __init__(self):
        self.idPublicacion = None
        self.titulo = None
        self.descripcion = None
        self.estado = None
        self.categoria = None
        self.publicador = None
        self.fechaCreacion = None
        self.fechaFin = None

