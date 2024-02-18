import time

from src.etl import ETL

def pipeline()->None:

	try:

		ETL("2019-06-22")

		print("ETL completado con exito")

		#time.sleep(300)

	except AttributeError as e:

		print(e)

		print("Reconectando en 5 segundos...")

		time.sleep(5)

		pipeline()

pipeline()