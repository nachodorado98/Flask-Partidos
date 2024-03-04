import pytest

from src.utilidades.utils import fecha_formato_correcto, fecha_anterior, fecha_siguiente, fecha_bonita

@pytest.mark.parametrize(["fecha"],
	[("fecha",),("1111",),("2019-01-111",),("2011-0216",),("22062019",),("2019/06/22",)]
)
def test_fecha_formato_incorrecto(fecha):

	assert not fecha_formato_correcto(fecha)

@pytest.mark.parametrize(["fecha"],
	[("2019-01-11",),("2011-02-16",),("2019-04-13",),("2019-06-22",)]
)
def test_fecha_formato_correcto(fecha):

	assert fecha_formato_correcto(fecha)

@pytest.mark.parametrize(["fecha", "dia_anterior"],
	[
		("2019-04-13", "2019-04-12"),
		("2019-06-22", "2019-06-21"),
		("2020-01-01", "2019-12-31"),
		("2019-06-01", "2019-05-31"),
		("2024-03-01", "2024-02-29")
	]
)
def test_fecha_anterior(fecha, dia_anterior):

	assert fecha_anterior(fecha)==dia_anterior

@pytest.mark.parametrize(["fecha", "dia_siguiente"],
	[
		("2019-04-12", "2019-04-13"),
		("2019-06-21", "2019-06-22"),
		("2019-12-31", "2020-01-01"),
		("2019-05-31", "2019-06-01"),
		("2024-02-29", "2024-03-01")
	]
)
def test_fecha_siguiente(fecha, dia_siguiente):

	assert fecha_siguiente(fecha)==dia_siguiente

@pytest.mark.parametrize(["fecha", "fecha_extendida"],
	[
		("2019-01-11", "Viernes 11 de Enero de 2019"),
		("2020-02-16", "Domingo 16 de Febrero de 2020"),
		("2019-04-13", "Sábado 13 de Abril de 2019"),
		("2019-06-22", "Sábado 22 de Junio de 2019")
	]
)
def test_fecha_bonita(fecha, fecha_extendida):

	assert fecha_bonita(fecha)==fecha_extendida