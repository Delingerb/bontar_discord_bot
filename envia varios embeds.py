import math
import pytz
from pytz import utc
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random


bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

api = "https://docs.tibiadata.com/"

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

#TESTING

selected_server = "Solidera"
guild_url = f"https://guildstats.eu/bosses?world={selected_server}&monsterName=&bossType=&rook=0"
not_wanted = ['Apprentice Sheng', 'Munster', 'Teleskor', 'Rottie the Rotworm', 'draptors', 'undead cavebears']

response = requests.get(guild_url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table", id="myTable")

data = pd.read_html(str(table))[0]
data.columns = data.columns.droplevel(0)
data = data.drop(['Type', 'Introduced', 'Expected in', 'Killed bosses', 'Killed players', 'Last seen', '#', 'Image'], axis=1)
data = data[~data['Boss name'].isin(not_wanted)]
pattern = r'^\d+(\.\d+)?%'
data = data[data['Possibility'].str.extract(pattern, expand=False).notnull()]
data['Possibility'] = data['Possibility'].str.rstrip('%')
data = data.convert_dtypes()
data['Possibility'] = data['Possibility'].astype('float64')

filtered_data = data[data['Possibility'] >= 14.9]

# Agregar una columna "Image URL" al DataFrame
filtered_data['Image URL'] = filtered_data['Boss name'].str.replace(' ', '_', regex=True)
filtered_data['Image URL'] = "https://guildstats.eu/images/bosses/" + filtered_data['Image URL'] + ".gif"

filtered_data['Boss name'] = filtered_data['Boss name'].str.capitalize()


sorted_data = filtered_data.sort_values('Possibility', ascending=False)

    
@slash_command(name="rare_boss", description="probability rare bosses of the day")
async def boss_command(ctx: SlashContext):
    # Obtener los datos filtrados
    filtered_data = sorted_data

    # Enviar un embed para cada jefe
    for _, row in filtered_data.iterrows():
        boss_name = row['Boss name']
        possibility = row['Possibility']
        image_url = row['Image URL']

        # Crear un embed para el jefe actual
        embed = Embed(title=boss_name, description=f"Probability: {possibility}%", color=random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=image_url)
        print(image_url)
        # Enviar el embed
        await ctx.send(embed=embed)




@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready papá")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))

# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")