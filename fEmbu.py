import pandas as pd
import requests
from bs4 import BeautifulSoup

# Descargar el contenido HTML de la página web
url = 'https://tibia.fandom.com/wiki/Imbuing'
response = requests.get(url)
html_content = response.text

# Crear un objeto BeautifulSoup para analizar el contenido HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Leer todas las tablas de la página utilizando pd.read_html()
tables = pd.read_html(url)

# Extraer los nombres de las tablas
table_names = []
h4_elements = soup.find_all('h4')

# Lista para almacenar las URL de las imágenes
image_urls = []

# Buscar las etiquetas <div class="floatleft"> que contienen las imágenes de los imbues
image_divs = soup.select('div.floatleft img')
for img_tag in image_divs:
    if 'data-src' in img_tag.attrs:
        # Obtener la URL de la imagen y agregarla a la lista
        image_url = img_tag['data-src']
        image_urls.append(image_url)

# Determinar el número mínimo de elementos <h4> y tablas
min_count = min(len(h4_elements), len(tables))

filtered_tables = []  # Lista para almacenar las tablas filtradas

for i in range(min_count):
    table = tables[i]
    if 'Available for' in table.columns:
        table.drop('Available for', axis=1, inplace=True)
    table = table.iloc[2:].copy()
    table['Name'] = h4_elements[i].text.strip("[]")
    cols = ['Name'] + [col for col in table.columns if col != 'Name']
    table = table[cols]
    table.iloc[:, 2] = table['Name'] + ' +' + table.iloc[:, 2].astype(str)
    
    filtered_tables.append(table)

# Unir todas las tablas filtradas en un solo DataFrame
merged_table = pd.concat(filtered_tables, ignore_index=True)

# Lista de columnas para unir los valores
columns_to_combine = ['Amount converted', 'Amount leeched', 'Extra Chance', 'Critical Damage increased by',
                      'Protection percent **', 'Protection percent', 'Chance', 'Speed increased',
                    'Extra Capacity', 'Skill increased', 'Shielding increased', 'Extra Magic Level']

# Crear una nueva columna llamada "Valores combinados"
merged_table['Upgrade'] = merged_table[columns_to_combine].apply(lambda row: ', '.join(row.dropna().astype(str)), axis=1)
merged_table.drop(['Amount converted', 'Amount leeched', 'Extra Chance', 'Critical Damage increased by',
                   'Protection percent **', 'Protection percent', 'Chance', 'Speed increased',
                'Extra Capacity', 'Skill increased', 'Shielding increased', 'Extra Magic Level'], axis=1, inplace=True)
merged_table.rename(columns={'Required Astral Sources': 'Required item'}, inplace=True)

# Agregar la lista de URLs de imágenes al DataFrame
merged_table['Image URL'] = image_urls

# Imprimir el DataFrame resultante
print(merged_table)
merged_table.to_excel('datos.xlsx', index=False)
#merged_table.to_excel('datos.xlsx', index=False)
#merged_table.to_json('datos.json', orient='records')