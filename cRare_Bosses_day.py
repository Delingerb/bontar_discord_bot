import math
import pytz
import random
import requests
import pandas as pd
from pytz import utc
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command
from interactions import SlashContext, slash_option, OptionType, Task, TimeTrigger
from interactions.ext.paginators import Paginator

bot = Client(intents=Intents.DEFAULT)
public_channel_id = 793316701155885056  # Buntar_public
role_id = "799964530301992961"  # Buntar
role_buntar = f"<@&{role_id}>"

def rare_bosses():
    selected_server = "Solidera"
    guild_url = f"https://guildstats.eu/bosses?world={selected_server}&monsterName=&bossType=&rook=0"
    not_wanted = ['Apprentice Sheng', 'Munster', 'Teleskor', 'Rottie the Rotworm', 'draptors', 
                'undead cavebears', 'midnight panthers', 'Zomba', 'Willi Wasp', 'Grand Mother Foulscale', 'The Blightfather']

    response = requests.get(guild_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", id="myTable")
    data = pd.read_html(str(table))[0]
    data.columns = data.columns.droplevel(0)
    data = data.drop(['Type', 'Introduced', 'Expected in', 'Killed bosses', 'Killed players', '#', 'Image'], axis=1)
    data = data[~data['Boss name'].isin(not_wanted)]
    pattern = r'^\d+(\.\d+)?%'
    data = data[data['Possibility'].str.extract(pattern, expand=False).notnull()]
    data['Possibility'] = data['Possibility'].str.rstrip('%')
    data['Possibility'] = data['Possibility'].astype('float64')
    filtered_data = data[data['Possibility'] >= 10]
    
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
    
    bosses_adjust_url = ['Yeti', 'Dharalion', 'Hairman The Huge', 'The Voice Of Ruin','Yaga The Crone']
    new_urls = ['https://www.tibiabosses.com/wp-content/uploads/2016/04/yeti.gif',
                'https://cdn.discordapp.com/attachments/1130606814061408354/1131524735793102920/Dharalion.gif',
                'https://cdn.discordapp.com/attachments/1130606814061408354/1131527491517960343/Hairman_the_Huge.gif',
                'https://cdn.discordapp.com/attachments/1130606814061408354/1131527861409435738/The_Voice_of_Ruin.gif',
                'https://cdn.discordapp.com/attachments/1130606814061408354/1131899098748944445/Yaga_the_Crone.gif']  # Lista de nuevas URLs correspondientes a los bosses
    for boss, new_url in zip(bosses_adjust_url, new_urls):
        data_copy.loc[data_copy['Boss name'] == boss, 'Image URL'] = new_url

    #data_copy.loc[:, 'Boss name'] = data_copy['Boss name'].str.capitalize()
    sorted_data = data_copy.sort_values('Possibility', ascending=False)
    return sorted_data

@slash_command(name="rare_bosses", description="Probability of rare bosses of the day")
async def boss_command(ctx: SlashContext):
    # Obtener los datos filtrados
    filtered_data = rare_bosses()

    boss_messages = []
    for _, row in filtered_data.iterrows():
        boss_name = row['Boss name']
        possibility = row['Possibility']
        image_url = row['Image URL']
        wiki_url = row['wiki URL']
        last_date = row['Last seen']

        # Crear un embed para el jefe actual
        embed = Embed(title=boss_name, 
                        description=f"Probability: **{possibility}%**\nThe boss was last seen {last_date}", 
                        color=random.randint(0, 0xFFFFFF), 
                        url=wiki_url)
        embed.set_thumbnail(url=image_url)
        boss_messages.append(embed)

    # Crear un paginador con la lista de mensajes y mostrarlo en Discord
    paginator = Paginator.create_from_embeds(bot, *boss_messages, timeout=120)
    await paginator.send(ctx)
    
@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready_Last")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))
    
#Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")