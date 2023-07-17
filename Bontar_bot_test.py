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


bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

api = "https://docs.tibiadata.com/"

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

#TESTING


def rare_bosses():
    selected_server = "Solidera"
    guild_url = f"https://guildstats.eu/bosses?world={selected_server}&monsterName=&bossType=&rook=0"
    not_wanted = ['Apprentice Sheng', 'Munster', 'Teleskor', 'Rottie the Rotworm', 'draptors']
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
    data = data.drop(['Type', 'Introduced', 'Expected in', 'Killed bosses', 'Killed players', 'Last seen', '#', 'Image'], axis=1)
    data = data[~data['Boss name'].isin(not_wanted)]
    pattern = r'^\d+(\.\d+)?%'
    data = data[data['Possibility'].str.extract(pattern, expand=False).notnull()]
    data['Possibility'] = data['Possibility'].str.rstrip('%')
    data = data.convert_dtypes()
    data['Possibility'] = data['Possibility'].astype('float64')
    data['Boss name'] = data['Boss name'].str.capitalize()
    filtered_data = data[data['Possibility'] >= 14.9]
    
    sorted_data = filtered_data.sort_values('Possibility', ascending=False)

    return sorted_data

    
@slash_command(name="rare_boss", description="probability rare bosses of the day")
async def boss_command(ctx: SlashContext):
    filtered_data = rare_bosses()

    embed = Embed(title="Probability rare bosses of the day", 
                color=0x6a93d5)

    for _, row in filtered_data.iterrows():
        boss_name = row['Boss name']
        possibility = row['Possibility']
        embed.add_field(name=boss_name, value=f"Chance: **{possibility}%**", inline=False)
        
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