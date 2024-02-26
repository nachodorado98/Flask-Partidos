from datetime import datetime, timedelta
from typing import List, Optional

from .config import FECHA_INICIO
from .database.conexion import Conexion

def obtenerFechaInicio()->str:

	con=Conexion()

	if con.tabla_vacia():

		inicio=FECHA_INICIO

	else:

		ultima_fecha=con.fecha_maxima()

		ultima_fecha_datetime=datetime.strptime(ultima_fecha, "%Y-%m-%d")

		inicio=(ultima_fecha_datetime+timedelta(days=1)).strftime("%Y-%m-%d")

	con.cerrarConexion()

	return inicio

def generarFechas(inicio:str, fin:str)->List[Optional[str]]:

	inicio_datetime=datetime.strptime(inicio, "%Y-%m-%d")

	fin_datetime=datetime.strptime(fin, "%Y-%m-%d")

	fechas=[]

	while inicio_datetime<=fin_datetime:

		fechas.append(inicio_datetime.strftime("%Y-%m-%d"))

		inicio_datetime+=timedelta(days=1)

	return fechas

def fechas_etl()->List[Optional[str]]:

	inicio=obtenerFechaInicio()

	fin=(datetime.now().date()-timedelta(days=3)).strftime("%Y-%m-%d")

	return generarFechas(inicio, fin)