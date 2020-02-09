import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import json


#enlazar selenium al navegador
navegador = webdriver.Chrome("C:/webDriver/chromedriver.exe")

#cargar la pagina en el navegador
navegador.get("https://elcomercio.pe/archivo/todas/2020-02-07/")

"""
    al revisar la pagina de el comercio,a la url de la linea 12, vi que la pagina mostraba, una cierta cantidad de articulos, luego al hacer scroll,
    hacia una peticion mediante un api(porfa, corrigeme si me equivoco) que carga el resto de articulos, estoy averiguando como hacer scraping cuando la data se muestra mediante un api.
"""
#ejecutar un javascript para que realice scroll a la pagina para conocer el tamaño del documento
PageLen = navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenPage=document.body.scrollHeight;return lenPage;")

final = False

#mientras no llegue al final de la pagina, hara scroll 
while(final == False):
    ultimaCuenta = PageLen
    #tiempo necesario para que cargue los datos restante
    time.sleep(3)

    PageLen = navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenPage=document.body.scrollHeight;return lenPage;")

    if ultimaCuenta == PageLen:
        final = True
        

#Una vez la pagina cargada, extraer el codigo fuente
codigoFuente = navegador.page_source

#cerramos el navegador
navegador.quit()

#parsearlo mediante beautiful soup
data = bs(codigoFuente, "html.parser")


datos = {}
datos["noticias"] = []

#una vex obtenido el html, buscar los tags correspondientes a cada elemento de la pagina (titulo, subtitulo, imagen)
for i in data.find_all('div', "story-item"):
    title = i.find('a',"story-item__title")
    subtitle = i.find('p',"story-item__subtitle")
    img = i.find('img', "story-item__img")
    datos["noticias"].append({
        "titulo" : title.text,
        "subtitulo" : subtitle.text,
        "imagen" : img["src"]
    })

#exportar los datos a un json
with open('noticias.json','w', encoding='utf-8') as file :
    json.dump(datos,file,indent=4)