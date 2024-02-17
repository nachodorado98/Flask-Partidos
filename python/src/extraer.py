import pandas as pd

from .scraper import Scraper
from .excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

def extraerData(fecha:str)->pd.DataFrame:

	try:

		scraper=Scraper(fecha)

		partidos=scraper.obtenerPartidos()

		return partidos

	except ErrorFechaFormato:

		print("Error en el formato fecha")

	except ErrorFechaPosterior:

		print("Error en la fecha introducida")

	except PaginaError:

		print("La pagina no esta accesible")

	except PartidosExtraidosError:

		print("No hay partidos disponibles para extraer")