import pytest
from datetime import datetime, timedelta
import pandas as pd

from src.etl import extraerData
from src.excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

@pytest.mark.parametrize(["fecha"],
	[("201906-22",), ("22/06/2019",), ("22062019",), ("2019-0622",), ("2019-06/22",)]
)
def test_extraer_data_error_fecha_formato(fecha):

	with pytest.raises(ErrorFechaFormato):

		extraerData(fecha)

@pytest.mark.parametrize(["dias"],
	[(1,), (10,), (100,), (1000,), (10000,)]
)
def test_extraer_data_error_fecha_posterior(dias):

	fecha=(datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")

	with pytest.raises(ErrorFechaPosterior):

		extraerData(fecha)

def test_extraer_data_error_partidos():

	with pytest.raises(PartidosExtraidosError):

		extraerData("1800-01-01")

def test_extraer_data():

	data=extraerData("2019-06-22")

	assert isinstance(data, pd.DataFrame)
	assert not data.empty