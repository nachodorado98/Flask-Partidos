from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from src.database.conexion import Conexion

from src.utilidades.utils import fecha_formato_correcto, fecha_anterior, fecha_siguiente, fecha_bonita

bp_inicio=Blueprint("inicio", __name__)

@bp_inicio.route("/", methods=["GET"])
def inicio():

	con=Conexion()

	fecha_maxima=con.fecha_maxima()

	fecha=request.args.get("fecha", default=fecha_maxima, type=str)

	if not fecha_formato_correcto(fecha):

		return redirect("/")

	dia_anterior, dia_siguiente=fecha_anterior(fecha), fecha_siguiente(fecha)

	partidos=con.obtenerPartidosFecha(fecha)

	con.cerrarConexion()

	return render_template("inicio.html",
							fecha=fecha,
							fecha_bonita=fecha_bonita(fecha),
							dia_anterior=dia_anterior,
							dia_siguiente=dia_siguiente,
							partidos=partidos)