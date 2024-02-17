import pandas as pd
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

from .scraper import Scraper
from .config import COMPETICIONES
from .excepciones import PartidosLimpiarError, ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

def extraerData(fecha:str)->pd.DataFrame:

	scraper=Scraper(fecha)

	partidos=scraper.obtenerPartidos()

	return partidos

def limpiarData(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Local"]=tabla["Local"].str.replace(r"\s[a-z]{2,3}$", "", regex=True)

	tabla["Visitante"]=tabla["Visitante"].str.replace(r"^[a-z]{2,3}\s", "", regex=True)

	def limpiarPublico(cantidad:str)->int:

		try:
		
			cantidad_str=cantidad.replace(",", "")
		
			return int(cantidad_str)

		except ValueError:

			return 0

	tabla["Asistencia"]=tabla["Asistencia"].apply(limpiarPublico)

	tabla_filtrada=tabla[tabla["Competicion"].isin(COMPETICIONES)]

	if tabla_filtrada.empty:

		raise PartidosLimpiarError("No hay partidos este dia")

	return tabla_filtrada.reset_index(drop=True)

def ETL(fecha:str)->None:

	try:

		data=extraerData(fecha)

		data_limpia=limpiarData(data)

		print(data_limpia)

	except Exception as e:

		print(e)