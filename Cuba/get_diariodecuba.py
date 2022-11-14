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

diariodecuba = pd.read_csv('diariodecuba.csv')
diariodecuba_url = "https://diariodecuba.com"

def get_diariodecuba(diariodecuba_url):
    sel=Selector(text=requests.get(diariodecuba_url).content)
    title = sel.xpath('//h2[@class="views-title-section"]/a/text()').extract()
    enlace = sel.xpath('//h2[@class="views-title-section"]/a/@href').extract()
    #resumen = sel.xpath('//p[@class="views-description"]/text()').extract()
    diariodecuba_df = pd.DataFrame({
        'titulo':title,
        'enlace':enlace})
    diariodecuba_new.append(diariodecuba_df)
    return diariodecuba_new

def get_complete_link(enlace):
    x = diariodecuba_url + enlace
    return(x)

def get_date(enlace):
    sel=Selector(text=requests.get(enlace).content)
    fecha = ' '.join(sel.xpath('//time[@class="date"]/text()').extract())
    return(fecha)

pattern = '\d{2}\s\w{3}\s\d{4}'    

def clean_date(fecha):
    x = ' '.join(re.findall(pattern, str(fecha)))
    return x

def get_text(enlace):
    sel=Selector(text=requests.get(enlace).content)
    texto = ' '.join(sel.xpath('//div[@class="content"]/p/text()').extract())
    return texto

sel=Selector(text=requests.get('https://diariodecuba.com/cuba/1668422911_43452.html').content)    
' '.join(sel.xpath('//div[@class="content"]/p/text()').extract())


diariodecuba_new = []
get_diariodecuba(diariodecuba_url)
diariodecuba_new = pd.concat(diariodecuba_new)    

diariodecuba_new['enlace'] = diariodecuba_new['enlace'].apply(get_complete_link)
diariodecuba_new['fecha'] = diariodecuba_new['enlace'].apply(get_date)
diariodecuba_new['fecha'] = diariodecuba_new['fecha'].apply(clean_date)
diariodecuba_new['texto'] = diariodecuba_new['enlace'].apply(get_text)
diariodecuba_new['pais'] = "Cuba"

diariodecuba = diariodecuba.append(diariodecuba_new).drop_duplicates(subset = ['enlace'])

diariodecuba.to_csv('diariodecuba.csv', index = False)
