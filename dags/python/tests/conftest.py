import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scraper import Scraper
from src.database.conexion import Conexion

@pytest.fixture
def scraper():

	return Scraper("2019-06-22")

@pytest.fixture
def conexion_basica():

	yield Conexion()

@pytest.fixture
def conexion(conexion_basica):

	conexion_basica.c.execute("DELETE FROM partidos")

	conexion_basica.confirmar()

	return conexion_basica