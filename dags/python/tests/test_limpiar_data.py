import pytest
import pandas as pd

from src.etl import extraerData, limpiarData
from src.excepciones import PartidosLimpiarError

def test_limpiar_partidos_error():

	data=extraerData("2022-12-19")

	with pytest.raises(PartidosLimpiarError):

		limpiarData(data)

def test_limpiar_partidos():

	data=extraerData("2019-06-22")

	data_limpia=limpiarData(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty