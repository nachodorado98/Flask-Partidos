import pytest
from datetime import datetime, timedelta
import time

from src.etl import ETL

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