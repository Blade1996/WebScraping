from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json
import os


driver = webdriver.Chrome("C:/webDriver/chromedriver")

data = {}
data["reportes"] = []



driver.get("https://elcomercio.pe/archivo/todas/2020-01-02")

contenido = driver.page_source

soup = BeautifulSoup(contenido, "html.parser")

for i in soup.find_all('div','story-item'):
    title = i.find('a',href=True, class_='story-item__title')
    subtitle = i.find('p', 'story-item__subtitle')
    img = i.find('img', 'story-item__img')

data["reportes"].append({
    "titulo" : title.text,
    "subtitulo" : subtitle.text,
    "imagen" : img["src"]

})

df = pd.DataFrame(data["reportes"]) 
df.to_json('Noticias.json')