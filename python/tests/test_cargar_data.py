import pytest

from src.etl import extraerData, limpiarData, cargarData

def test_cargar_partidos(conexion):

	data=extraerData("2019-06-22")

	data_limpia=limpiarData(data)

	cargarData(data_limpia)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==2