def test_tabla_partidos_llena(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert conexion.c.fetchall()

def test_obtener_partidos_no_existen(conexion):

	assert conexion.obtenerPartidosFecha("2019-06-22") is None

def test_obtener_partidos_existen(conexion):

	partidos=conexion.obtenerPartidosFecha("2024-02-16")

	for partido in partidos:

		assert partido[2]=="16-02-2024"