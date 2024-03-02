import pytest
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs4
import pandas as pd
import time

from src.scraper import Scraper
from src.excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

def test_pausa():

	time.sleep(60)

@pytest.mark.parametrize(["fecha"],
	[("201906-22",), ("22/06/2019",), ("22062019",), ("2019-0622",), ("2019-06/22",)]
)
def test_crear_objeto_scraper_error_formato(fecha):

	with pytest.raises(ErrorFechaFormato):

		Scraper(fecha)

@pytest.mark.parametrize(["dias"],
	[(1,), (10,), (100,), (1000,), (10000,)]
)
def test_crear_objeto_scraper_error_fecha_posterior(dias):

	fecha=(datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")

	with pytest.raises(ErrorFechaPosterior):

		Scraper(fecha)

@pytest.mark.parametrize(["fecha"],
	[("2019-06-22",), ("2019-04-13",), (datetime.now().strftime("%Y-%m-%d"),)]
)
def test_crear_objeto_scraper(fecha):

	scraper=Scraper(fecha)

	assert scraper.obtenerFecha()==fecha

def test_scraper_realizar_peticion(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_contenido_a_tablas(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	assert isinstance(tablas, list)

def test_scraper_titulo(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	titulo=scraper._Scraper__obtenerTitulo(tabla)

	assert isinstance(titulo, str)

def test_scraper_titulo_tabla(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	titulo_tabla=scraper._Scraper__obtenerTituloTabla(tabla)

	assert isinstance(titulo_tabla, str)

def test_scraper_ambos_titulos(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	titulo=scraper._Scraper__obtenerTitulo(tabla)

	titulo_tabla=scraper._Scraper__obtenerTituloTabla(tabla)

	assert titulo==titulo_tabla

def test_scraper_columnas(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	columnas=scraper._Scraper__obtenerColumnas(tabla)

	assert isinstance(columnas, list)
	assert len(columnas)==13

def test_scraper_contenido_filas(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	contenido_filas=scraper._Scraper__obtenerContenidoFilas(tabla)

	assert isinstance(contenido_filas, list)

	for fila in contenido_filas:

		assert isinstance(fila, list)

def test_scraper_limpiar_tabla(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tabla=tablas[0]

	tabla_limpia=scraper._Scraper__limpiarTabla(tabla)

	assert isinstance(tabla_limpia, pd.DataFrame)

def test_scraper_obtener_data_limpia(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	tablas_limpias=scraper._Scraper__obtenerDataLimpia(tablas)

	assert isinstance(tablas_limpias, pd.DataFrame)
	assert not tablas_limpias.empty

def test_scraper_obtener_data_limpia_error():

	scraper=Scraper("1800-01-01")

	contenido=scraper._Scraper__realizarPeticion()

	tablas=scraper._Scraper__contenido_a_tablas(contenido)

	with pytest.raises(PartidosExtraidosError):

		scraper._Scraper__obtenerDataLimpia(tablas)

def test_scraper_obtener_partidos(scraper):

	data=scraper.obtenerPartidos()

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

def test_scraper_obtener_partidos_error():

	scraper=Scraper("1800-01-01")

	with pytest.raises(PartidosExtraidosError):

		scraper.obtenerPartidos()