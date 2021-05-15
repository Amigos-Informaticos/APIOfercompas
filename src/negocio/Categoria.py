from enum import Enum

from sqlalchemy import Column, Integer, String

from src.datos.Conexion import Conexion


class Categoria(Conexion):
	__tablename__ = "Categoria"

	idCategoria: Column = Column(Integer(), primary_key=True, nullable=False)
	categoria: Column = Column(String(50), nullable=False)


	TECNOLOGIA = 1
	MODA_MUJER = 2
	MODA_HOMBRE = 3
	HOGAR = 4
	MASCOTAS = 5
	VIAJE = 6
	ENTRETENIMIENTO = 7
	COMIDA_BEBIDA = 8
