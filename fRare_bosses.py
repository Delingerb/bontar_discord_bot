import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests


def rare_bosses():
    selected_server = "Solidera"
    guild_url = f"https://guildstats.eu/bosses?world={selected_server}&monsterName=&bossType=&rook=0"
    not_wanted = ['Apprentice Sheng', 'Munster', 'Teleskor', 'Rottie the Rotworm', 'draptors', 'undead cavebears', 'midnight panthers']
    boss_name = 'man in the cave'

    response = requests.get(guild_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", id="myTable")

    img_tag = soup.find("img", alt=boss_name)
    if img_tag:
        img_src = img_tag.get("src")
        img_url = f"https://guildstats.eu/{img_src}"
    else:
        return f"No se encontró la imagen para el boss {boss_name}"

    data = pd.read_html(str(table))[0]
    data.columns = data.columns.droplevel(0)
    data = data.drop(['Type', 'Introduced', 'Expected in', 'Killed bosses', 'Killed players', '#', 'Image'], axis=1)
    data = data[~data['Boss name'].isin(not_wanted)]
    pattern = r'^\d+(\.\d+)?%'
    data = data[data['Possibility'].str.extract(pattern, expand=False).notnull()]
    data['Possibility'] = data['Possibility'].str.rstrip('%')
    data['Possibility'] = data['Possibility'].astype('float64')

    filtered_data = data[data['Possibility'] >= 15]
    
    # Crear una copia explícita del DataFrame
    data_copy = filtered_data.copy()
    
    bosses_to_edit = ['yetis']  # Lista de nombres de los bosses a editar
    new_names = ['Yeti']  # Lista de nuevos nombres correspondientes a los bosses
    
    for boss, new_name in zip(bosses_to_edit, new_names):
        data_copy.loc[data_copy['Boss name'] == boss, 'Boss name'] = new_name
    
    # Agregar una columna "wiki" a la copia
    data_copy['wiki URL'] = "https://tibia.fandom.com/wiki/" + data_copy['Boss name']
    data_copy['wiki URL'] = data_copy['wiki URL'].str.replace(' ', '_', regex=True)
    
        # Agregar una columna "Image URL" a la copia
    data_copy['Image URL'] = "https://guildstats.eu/images/bosses/" + data_copy['Boss name'] + ".gif"
    data_copy['Image URL'] = data_copy['Image URL'].str.replace(' ', '_', regex=True)
    
    bosses_adjust_url = ['Yeti']
    new_urls = ['https://www.tibiabosses.com/wp-content/uploads/2016/04/yeti.gif']  # Lista de nuevas URLs correspondientes a los bosses
    for boss, new_url in zip(bosses_adjust_url, new_urls):
        data_copy.loc[data_copy['Boss name'] == boss, 'Image URL'] = new_url

    data_copy.loc[:, 'Boss name'] = data_copy['Boss name'].str.capitalize()
        
    sorted_data = data_copy.sort_values('Possibility', ascending=False)

    return sorted_data

print(rare_bosses())

#rare_bosses().to_excel('rare_bosses2.xlsx', index=False)
