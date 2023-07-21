import math
import pytz
from pytz import utc
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from interactions import SlashCommandOption, SlashCommandChoice
import re

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

df = pd.read_excel('imbue_data.xlsx')
wiki_base_url = "https://tibia.fandom.com/wiki/"
wiki_icon="https://static.wikia.nocookie.net/tibia/images/6/6e/TibiaWiki.gif/revision/latest/thumbnail/width/360/height/360?cb=20150121085821&path-prefix=en"
# Obtener los nombres del DataFrame en el orden requerido
desired_order = ['Critical Hit', 'Mana Leech', 'Life Leech', 'Magic Level', 'Capacity', 'Axe Fighting', 'Sword Fighting', 'Club Fighting', 'Distance Fighting', 'Paralysis Deflection', 'Death Protection', 'Earth Protection', 'Fire Protection', 'Ice Protection', 'Energy Protection', 'Holy Protection', 'Fire Damage', 'Earth Damage', 'Ice Damage', 'Energy Damage', 'Death Damage', 'Walking Speed', 'Shielding']
sorted_names = sorted(df['Name'], key=lambda x: desired_order.index(x) if x in desired_order else len(desired_order))

@slash_command(
    name="imbue",
    description="imbue options",
    options=[
        SlashCommandOption(
            name="option",
            description="Options",
            required=True,
            type=OptionType.STRING,
            choices=[
                {
                    "name": name,
                    "value": name
                }
                for name in sorted_names
            ]
        )
    ]
)

async def imbue_function(ctx: SlashContext, option: str):
    selected_data = df[df['Name'] == option]  # Filtrar los datos que coinciden con el imbue seleccionado
    if not selected_data.empty:
        # Iterar sobre las filas de los datos seleccionados
        for _, row in selected_data.iterrows():
            # Obtener los valores de cada columna para la fila actual
            imbue_type = row['Name']
            imbuement_name = row['Imbuement Name']
            required_items = row['Required item']
            required_items_list = required_items.split(', ')
            frequired_items = "\n".join(required_items_list)
            upgrade = row['Upgrade']
            imbue_img = row['Image URL']
            imbue_url = "https://tibia.fandom.com/wiki/"+imbuement_name.replace(' ', '_')
            
    embed = Embed(title=imbuement_name,
                url=imbue_url,
                color="#{:06x}".format(random.randint(0, 0xFFFFFF))
                    )
    embed.set_thumbnail(url=imbue_img)
    embed.set_author(name="Tibia Wiki", url=wiki_base_url, icon_url=wiki_icon)
    embed.add_field(name="Upgrade:", value=upgrade, inline=True)
    embed.add_field(name="Required Item:", value=frequired_items, inline=True)
    embed.set_footer("Imbuing is the action of temporarily boosting an equipment item using Astral Sources.")
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
