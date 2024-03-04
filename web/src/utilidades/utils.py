from datetime import datetime, timedelta

# Funcion para comprobar si la fecha tiene el formato correcto
def fecha_formato_correcto(fecha:str)->bool:

	try:

		fecha_formato=datetime.strptime(fecha, "%Y-%m-%d")

		return True

	except ValueError:

		return False

# Funcion para obtener la fecha anterior a una fecha
def fecha_anterior(fecha:str)->str:

	fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d")

	fecha_anterior=fecha_datetime-timedelta(days=1)

	return fecha_anterior.strftime("%Y-%m-%d")

# Funcion para obtener la fecha siguiente a una fecha
def fecha_siguiente(fecha:str)->str:

	fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d")

	fecha_anterior=fecha_datetime+timedelta(days=1)

	return fecha_anterior.strftime("%Y-%m-%d")

# Funcion para obtener la fecha en una cadena mas bonita
def fecha_bonita(fecha:str)->str:

    fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d")
    
    dias_semana=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    meses=["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    dia_semana=dias_semana[fecha_datetime.weekday()]

    nombre_mes=meses[fecha_datetime.month]

    return f"{dia_semana} {fecha_datetime.day} de {nombre_mes} de {fecha_datetime.year}"