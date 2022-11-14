# Load necessary libraries
from scrapy import Selector
import requests
import pandas as pd
import numpy as np
import os
import datetime as dt
import locale
import time
import re
from datetime import datetime

listin_diario = pd.read_csv('listin_diario.csv')

listin_diario_url = 'https://listindiario.com/'
sel=Selector(text=requests.get(listin_diario_url).content)
enlace1 = sel.xpath('//div[@class="topleftmain_titulo"]/a/@href').extract()
enlace2 = sel.xpath('//div[@class="topcentermain_titulo"]/a/@href').extract()

enlaces = enlace1 + enlace2
    
enlace_completo = []
for enlace in enlaces:
    enlace_completo.append('https://listindiario.com' + enlace)
    
listin_diario_nuevo = pd.DataFrame({
    'enlace':enlace_completo})

def get_title(enlace):
    sel=Selector(text=requests.get(enlace).content)
    titulo = sel.xpath('//h1[@class="art_titulo"]/text()').extract()
    return titulo

def clean_title(titulo):
    cleaned_title = ' '.join(titulo).strip()
    return cleaned_title
    
def get_date(enlace):
    sel=Selector(text=requests.get(enlace).content)
    fecha = sel.xpath('//div[@class="art_sly_1"]/span/text()').extract()
    return fecha

def clean_date(fecha):
    cleaned_fecha = ' '.join(fecha).strip()
    return cleaned_fecha

def get_text(enlace):
    sel=Selector(text=requests.get(enlace).content)
    texto = ' '.join(sel.xpath('//div[@id="ArticleBody"]/p/text()').extract())
    return texto

listin_diario_nuevo['titulo'] = listin_diario_nuevo['enlace'].apply(get_title)    
listin_diario_nuevo['titulo'] = listin_diario_nuevo['titulo'].apply(clean_title)
listin_diario_nuevo['fecha'] = listin_diario_nuevo['enlace'].apply(get_date)
listin_diario_nuevo['fecha'] = listin_diario_nuevo['fecha'].apply(clean_date)
listin_diario_nuevo['texto'] = listin_diario_nuevo['enlace'].apply(get_text)
listin_diario_nuevo['pais'] = 'República Dominicana'

listin_diario = listin_diario.append(listin_diario_nuevo).drop_duplicates(subset = ['enlace'])

#listin_diario_nuevo.to_csv('listin_diario.csv', index = False)
