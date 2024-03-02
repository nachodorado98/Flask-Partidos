import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	#Metodo para insertar un partido
	def insertarPartido(self, partido:List[str])->None:

		self.c.execute("""INSERT INTO partidos (competicion, ronda, fecha, hora, local, marcador, visitante,
							publico, sede)
							VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							tuple(partido))

		self.confirmar()

	#Metodo para insertar multiples partidos
	def insertarPartidos(self, partidos:List[List])->None:

		for partido in partidos:

			self.insertarPartido(partido)

	# Metodo para saber si la tabla esta vacia
	def tabla_vacia(self)->bool:

		self.c.execute("""SELECT *
							FROM partidos""")

		return True if not self.c.fetchall() else False

	# Metodo para obtener la fecha maxima de la tabla
	def fecha_maxima(self)->Optional[str]:

		self.c.execute("""SELECT MAX(fecha) as fecha_maxima
							FROM partidos""")

		fecha_maxima=self.c.fetchone()["fecha_maxima"]

		return None if fecha_maxima is None else fecha_maxima.strftime("%Y-%m-%d")