import time

from src.etl import realizarETL

def pipeline()->None:

	try:

		realizarETL()

		#time.sleep(300)

	except AttributeError as e:

		print(e)

		print("Reconectando en 5 segundos...")

		time.sleep(5)

		pipeline()

pipeline()