import pytest
from datetime import datetime, timedelta
import time

from src.etl import ETL, realizarETL

@pytest.mark.parametrize(["fecha"],
	[("201906-22",), ("22/06/2019",), ("22062019",), ("2019-0622",), ("2019-06/22",)]
)
def test_etl_error_fecha_formato(conexion, fecha):

	ETL(fecha)

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["dias"],
	[(1,), (10,), (100,), (1000,), (10000,)]
)
def test_etl_error_fecha_posterior(conexion, dias):

	fecha=(datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")

	ETL(fecha)

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_etl_error_partidos(conexion):

	ETL("1800-01-01")

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_etl_error_limpiar_partidos(conexion):

	ETL("2022-12-19")

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_etl(conexion):

	ETL("2019-06-22")

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==2

def test_pausa1():

	time.sleep(30)

@pytest.mark.parametrize(["numero_etls"],
	[(2,),(6,),(5,),(3,)]
)
def test_etl_multiples(conexion, numero_etls):

	for _ in range(numero_etls):

		ETL("2019-06-22")

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==2*numero_etls

def test_pausa2():

	time.sleep(60)

def test_realizar_etl_tabla_vacia(conexion):

	assert conexion.tabla_vacia()

	realizarETL()

	conexion.c.execute("SELECT * FROM partidos ORDER BY fecha")

	partidos=conexion.c.fetchall()

	assert partidos[0]["fecha"].strftime("%Y-%m-%d")=="2024-01-01"
	assert partidos[-1]["fecha"].strftime("%Y-%m-%d")==(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

def test_pausa3():

	time.sleep(60)

@pytest.mark.parametrize(["fecha"],
	[
		("2024-02-11",),
		("2024-02-14",),
		("2024-02-08",),
		((datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d"),)
	]
)
def test_realizar_etl_fechas(conexion_basica, fecha):

	assert not conexion_basica.tabla_vacia()

	conexion_basica.c.execute("SELECT * FROM partidos")

	partidos_totales=conexion_basica.c.fetchall()

	cantidad_partidos_totales=len(partidos_totales)

	conexion_basica.c.execute("DELETE FROM partidos WHERE fecha>=%s", (fecha,))

	conexion_basica.confirmar()

	conexion_basica.c.execute("SELECT * FROM partidos")

	partidos_actuales=conexion_basica.c.fetchall()

	cantidad_partidos_actuales=len(partidos_actuales)

	assert cantidad_partidos_totales>cantidad_partidos_actuales

	cantidad_partidos_eliminados=cantidad_partidos_totales-cantidad_partidos_actuales

	for partido in partidos_actuales:

		assert not partido["fecha"].strftime("%Y-%m-%d")>fecha

	realizarETL()

	conexion_basica.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion_basica.c.fetchall()

	cantidad_partidos_nuevos=len(partidos_nuevos)

	assert cantidad_partidos_nuevos==cantidad_partidos_totales
	assert cantidad_partidos_nuevos-cantidad_partidos_actuales==cantidad_partidos_eliminados

	time.sleep(5)

def test_realizar_etl_actualizado(conexion_basica):

	assert not conexion_basica.tabla_vacia()

	conexion_basica.c.execute("SELECT * FROM partidos")

	partidos_actuales=conexion_basica.c.fetchall()

	realizarETL()

	conexion_basica.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion_basica.c.fetchall()

	assert len(partidos_actuales)==len(partidos_nuevos)

def test_pausa4():

	time.sleep(60)