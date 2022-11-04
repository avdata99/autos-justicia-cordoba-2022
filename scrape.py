import csv
import json
import os
import string
from time import sleep
from bs4 import BeautifulSoup as bs
import requests


valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}
url = 'https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/VehiculosSecuestrados.aspx'
response = requests.get(url, headers=headers)
soup = bs(response.text, 'html.parser')

marcas_sel = soup.find('select', {'id': 'ddlModelo'})
marcas_opt = marcas_sel.find_all('option')
print(marcas_opt)

marcas = {marca['value']: marca.text for marca in marcas_opt if marca['value'] != ''}

page_size = 100
params = {
    "idModelo": None,
    "pageSize": page_size,
    "pageIndex": 0,
    "sortColumn": None,
    "sortDirection": "asc"
}

results_file = open('resultados.csv', 'w')
fieldnames = [
    "Marca",
    "Marca ID",
    "IDRegistro",
    "TipoVehiculo",
    "Modelo",
    "Color",
    "Destino",
    "LegajoInterno",
    "DestinoFecha",
    "Dominio",
]
results_writer = csv.DictWriter(results_file, fieldnames)
results_writer.writeheader()

post_url = 'https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/VehiculosSecuestrados.aspx/Search'
for marca_id, marca_nombre in marcas.items():
    page_index = 0
    while True:
        print(f'Buscando {marca_nombre}-{marca_id}-{page_index} ...')
        file_name = f'{marca_nombre}.{marca_id}-{page_index}.json'
        file_name = f'data/' + ''.join(c for c in file_name if c in valid_chars)
        if os.path.exists(file_name):
            print(f'Ya existe {file_name}')
            data = json.load(open(file_name))
        else:
            print(f'Creando {file_name}')
            params["idModelo"] = marca_id
            params["pageIndex"] = page_index
            response = requests.post(post_url, headers=headers, json=params)
            data = response.json()
            f = open(file_name, 'w')
            f.write(json.dumps(data, indent=4))
            f.close()
            sleep(2)

        for auto in data['d']['ObjectData']:
            auto.update({
                "Marca": marca_nombre,
                "Marca ID": marca_id,
            })
            results_writer.writerow(auto)
        if len(data['d']['ObjectData']) < page_size:
            break
        page_index += 1

results_writer.close()
results_file.close()
print('TERMINADO')
