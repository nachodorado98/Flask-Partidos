import requests
from datetime import datetime, date
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .config import URL
from .excepciones import ErrorFechaFormato, ErrorFechaPosterior, PaginaError, PartidosExtraidosError

class Scraper:

    def __init__(self, fecha:str)->None:

        self.fecha=self.__comprobarFecha(fecha)
        self.url_scrapear=URL+self.fecha

    def __comprobarFecha(self, fecha:str)->str:

        try:

            fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d").date()

        except ValueError:

            raise ErrorFechaFormato("Error de formato de fecha. El formato debe ser yyyy-mm-dd")

        if fecha_datetime>date.today():

             raise ErrorFechaPosterior("La fecha no puede ser posterior al día de hoy")

        return fecha

    def obtenerFecha(self)->str:

        return self.fecha

    def __realizarPeticion(self)->bs4:

        peticion=requests.get(self.url_scrapear)

        if peticion.status_code!=200:

            print(f"Codigo de estado de la peticion: {peticion.status_code}")
            
            raise PaginaError("Error en la pagina")

        return bs4(peticion.text,"html.parser")

    def __contenido_a_tablas(self, contenido:bs4)->List[bs4]:

        return contenido.find_all("div", class_="table_wrapper tabbed")

    def __obtenerTitulo(self, tabla:bs4)->str:
    
        return tabla.find("span").text.strip(r'">')

    def __obtenerTituloTabla(self, tabla:bs4)->str:
        
        return tabla.find("table").find("a").text

    def __obtenerColumnas(self, tabla:bs4)->List[str]:
    
        cabecera=tabla.find("table").find("thead")
        
        columnas=cabecera.find("tr").find_all("th")
        
        return [columna.text for columna in columnas]

    def __obtenerContenidoFilas(self, tabla:bs4)->List[List]:

        filas=tabla.find("table").find("tbody").find_all("tr")

        def limpiarFila(fila:bs4)->List[str]:
    
            head=fila.find("th").text
                
            fila_contenido=fila.find_all("td")

            return [head]+[valor.text for valor in fila_contenido]
        
        return [limpiarFila(fila) for fila in filas]  

    def __limpiarTabla(self, tabla:bs4)->pd.DataFrame:
    
        titulo=self.__obtenerTitulo(tabla)
        
        titulo_tabla=self.__obtenerTituloTabla(tabla)
        
        assert titulo==titulo_tabla

        columnas=self.__obtenerColumnas(tabla)

        contenido_filas=self.__obtenerContenidoFilas(tabla)
        
        df=pd.DataFrame(contenido_filas, columns=columnas)
        
        df["Competicion"]=titulo
        
        if "Sem." not in list(df.columns):
            
            df["Sem."]="-"
        
        return df[["Competicion", "Ronda", "Sem.", "Hora", "Local", "Marcador", "Visitante", "Asistencia", "Sedes"]]

    def __obtenerDataLimpia(self, tablas:List[bs4])->Optional[pd.DataFrame]:

        tablas_limpias=[self.__limpiarTabla(tabla) for tabla in tablas]

        if not tablas_limpias:

            raise PartidosExtraidosError("No hay partidos disponibles para extraer")

        return pd.concat(tablas_limpias).reset_index(drop=True)

    def obtenerPartidos(self)->pd.DataFrame:

        contenido=self.__realizarPeticion()

        tablas=self.__contenido_a_tablas(contenido)

        return self.__obtenerDataLimpia(tablas)