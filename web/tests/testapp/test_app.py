import pytest
from datetime import datetime

from src.utilidades.utils import fecha_bonita

@pytest.mark.parametrize(["fecha"],
	[("fecha",),("1111",),("2019-01-111",),("2011-0216",),("22062019",),("2019/06/22",)]
)
def test_pagina_inicial_formato_incorrecto(cliente, fecha):

	respuesta=cliente.get(f"/?fecha={fecha}")

	contenido=respuesta.data.decode()

	respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

def test_pagina_inicial_formato_correcto(cliente):

	respuesta=cliente.get("/?fecha=2024-02-16")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "No hay partidos este dia" not in contenido
	assert "Partidos Del Viernes 16 de Febrero de 2024" in contenido
	assert "16-02-2024" in contenido

@pytest.mark.parametrize(["fecha", "fecha_tabla"],
	[
		("2019-06-22", "22-06-2019"),
		("2024-02-08", "08-02-2024"),
		("2024-01-09", "09-01-2024")
	]
)
def test_pagina_inicial_partidos_no_existen(cliente, fecha, fecha_tabla):

	respuesta=cliente.get(f"/?fecha={fecha}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "No hay partidos este dia" in contenido
	assert "Partidos Del "+fecha_bonita(fecha) in contenido
	assert fecha_tabla not in contenido

def test_pagina_inicial_fecha_maxima(cliente, conexion):

	fecha_maxima=conexion.fecha_maxima()

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Partidos Del "+fecha_bonita(fecha_maxima) in contenido
	assert 'class="boton-anterior"' in contenido
	assert 'class="boton-anterior boton-anterior-deshabilitado"' not in contenido
	assert 'class="boton-siguiente"' not in contenido
	assert 'class="boton-siguiente boton-siguiente-deshabilitado"' in contenido

def test_pagina_inicial_fecha_minima(cliente, conexion):

	fecha_minima=conexion.fecha_minima()

	respuesta=cliente.get(f"/?fecha={fecha_minima}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Partidos Del "+fecha_bonita(fecha_minima) in contenido
	assert 'class="boton-anterior"' not in contenido
	assert 'class="boton-anterior boton-anterior-deshabilitado"' in contenido
	assert 'class="boton-siguiente"' in contenido
	assert 'class="boton-siguiente boton-siguiente-deshabilitado"' not in contenido