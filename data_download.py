import pandas as pd 
import requests
from bs4 import BeautifulSoup
import os 
from tqdm import tqdm

raw_folder_path = "raw"
#Se comprueba que no exista el folder 'raw'
if not os.path.isdir(raw_folder_path):
    os.mkdir(raw_folder_path)
    print(f"Se creó el directorio {raw_folder_path}")
else:
    print("El folder 'raw' ya existe en este directorio")

#Se almacenan los links en un diccionario
url = 'https://www.aerocivil.gov.co/atencion/estadisticas-de-las-actividades-aeronauticas/bases-de-datos'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

url_dict = {}
for link in soup.find_all('a'):
    if link.get('href') is not None and "Destino" in link.get('href'):
        url_dict[link.get('href').split("Destino")[-1].strip()] = link.get('href')

#Se seleccionan unicamente los ultimos 20 años de datos
valid_years= [str(x) for x in range(2003,2024)]
url_dict_updated={}
for key in url_dict.keys():
    for year in valid_years:
        if year in key:
            url_dict_updated[key] = url_dict[key]

print("Descargando archivos: ")
for key in tqdm(url_dict_updated.keys()):
    file_path =  os.path.join(raw_folder_path, key)
    if not os.path.exists(file_path):
        print(key)
        response = requests.get(url_dict[key])
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        continue 