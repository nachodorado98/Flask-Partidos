import time

from .etl import realizarETL

def pipeline()->None:

	try:

		realizarETL()

	except AttributeError as e:

		print(e)

		print("Reconectando en 5 segundos...")

		time.sleep(5)

		pipeline()