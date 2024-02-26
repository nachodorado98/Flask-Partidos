import pytest
from datetime import datetime, timedelta

from src.utils import obtenerFechaInicio, generarFechas, fechas_etl

def test_obtener_fecha_inicio_tabla_vacia(conexion):

	assert obtenerFechaInicio()=="2024-01-01"

def test_obtener_fecha_inicio_tabla_registro(conexion):

	partido=["Champions", "Final", "2019-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]

	conexion.insertarPartido(partido)

	assert obtenerFechaInicio()=="2019-06-23"

def test_obtener_fecha_inicio_tabla_registros(conexion):

	partidos=[["Champions", "Final", "2019-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2020-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2019-07-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2023-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2024-04-13","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2022-06-13","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]]

	conexion.insertarPartidos(partidos)

	assert obtenerFechaInicio()=="2024-04-14"

@pytest.mark.parametrize(["inicio", "fin"],
	[
		("2019-06-22", "2019-04-13"),
		("2023-06-22", "2019-04-13"),
		("2019-06-22", "2019-06-21"),
		("2019-07-22", "2019-04-13"),
		("2019-06-22", "2019-06-13")
	]
)
def test_generar_fechas_inicio_superior(inicio, fin):

	assert not generarFechas(inicio, fin)

def test_generar_fechas_inicio_fin_iguales():

	assert len(generarFechas("2019-06-22", "2019-06-22"))==1

def test_fechas_etl_tabla_vacia(conexion):

	fechas=fechas_etl()

	assert fechas[0]=="2024-01-01"
	assert fechas[-1]==(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

def test_fechas_etl_tabla_registro(conexion):

	partido=["Champions", "Final", "2024-01-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]

	conexion.insertarPartido(partido)

	fechas=fechas_etl()

	assert fechas[0]=="2024-01-23"
	assert fechas[-1]==(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

def test_fechas_etl_tabla_registros(conexion):

	partidos=[["Champions", "Final", "2019-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2020-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2019-07-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2023-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2024-01-21","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2022-06-13","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]]

	conexion.insertarPartidos(partidos)

	fechas=fechas_etl()

	assert fechas[0]=="2024-01-22"
	assert fechas[-1]==(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

def test_fechas_etl_tabla_dia_anterior(conexion):

	dia_anterior=(datetime.now().date()-timedelta(days=4)).strftime("%Y-%m-%d")
	dia_ultimo=(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

	partidos=[["Champions", "Final", "2019-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2020-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2019-07-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2023-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", dia_anterior,"21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2022-06-13","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]]

	conexion.insertarPartidos(partidos)

	fechas=fechas_etl()

	assert fechas[0]==dia_ultimo
	assert fechas[-1]==dia_ultimo
	assert len(fechas)==1

def test_fechas_etl_tabla_dia_ultimo(conexion):

	dia_ultimo=(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

	partidos=[["Champions", "Final", "2019-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2020-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2019-07-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2023-06-22","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", dia_ultimo,"21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"],
				["Champions", "Final", "2022-06-13","21:00", "ATM", "5-0", "Madrid", 12345, "Calderon"]]

	conexion.insertarPartidos(partidos)

	assert not fechas_etl()