from .etl import extraerData, limpiarData
from .excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

def ETL(fecha:str)->None:

	data=extraerData(fecha)

	data_limpia=limpiarData(data)

	print(data_limpia)