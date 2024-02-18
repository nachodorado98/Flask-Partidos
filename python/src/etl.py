import pandas as pd
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

from .scraper import Scraper
from .config import COMPETICIONES
from .excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError, PartidosLimpiarError
from .database.conexion import Conexion

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

def cargarData(tabla:pd.DataFrame)->None:

	con=Conexion()

	partidos=tabla.values.tolist()

	con.insertarPartidos(partidos)

	con.cerrarConexion()

def ETL(fecha:str)->None:

	try:

		data=extraerData(fecha)

		data_limpia=limpiarData(data)

		cargarData(data_limpia)

	except ErrorFechaFormato as e:

		print(e)

	except ErrorFechaPosterior as e:

		print(e)

	except PaginaError as e:

		print(e)

	except PartidosExtraidosError as e:

		print(e)

	except PartidosLimpiarError as e:

		print(e)