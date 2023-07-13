import math
import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType


bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

api = "https://docs.tibiadata.com/"


#functions
#CALCULATE EXP
def calculate_exp(current_lvl, desired_lvl):
    total_experience = 0

    if current_lvl >= desired_lvl:
        message = "Warning: The current level must be lower than the desired level."
        return message

    for level in range(current_lvl, desired_lvl):
        level_experience = 50 * level ** 2 - 150 * level + 200
        total_experience += level_experience

    formatted_experience = "{:,}".format(total_experience)
    message = f"To level up from {current_lvl} to {desired_lvl}, you need **{formatted_experience}** experience points."
    return message
#CALCULATE EXP/

# Obtener el contenido HTML de la página web
wikiurl = "https://tibia.fandom.com/wiki/Main_Page"
response = requests.get(wikiurl)
html_content = response.text

# Crear un objeto BeautifulSoup para analizar el contenido HTML
soup = BeautifulSoup(html_content, "html.parser")
# Encontrar el elemento con la clase "compact-box compact-box-boss no-pseudoelements-container"
elemento = soup.find("div", class_="compact-box compact-box-boss no-pseudoelements-container")
# Obtener el título
boss_name = elemento.find("b").text.strip()
#Hp **************
hp_span = elemento.find("span", class_="creature-stats-hp")
hp_value = hp_span.find("span", class_="tibiatext").text
# Exp******************
exp_span = elemento.find("span", class_="creature-stats-exp")
exp_value = exp_span.find("span", class_="tibiatext").text
# obtener Imagen ******************
image_span = elemento.find("span", class_="no-pseudoelements-container")
boss_img = image_span.find("img")["data-src"]





@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="hola_test", description="My first command :)")
async def hola_test(ctx: SlashContext):
    await ctx.send("Hello todo bien?")

@slash_command(name="boss", description="Boss Boosted del día.")
async def boss(ctx:SlashContext):
    embed = Embed(title= boss_name,
                url="https://tibia.fandom.com/wiki/" + boss_name.replace(" ", "_"),
                  description="**Vida**: "+ hp_value + "\n" + " **Experiencia**: " + exp_value,
                color="#ffffff")
    embed.set_thumbnail(url= boss_img)
    embed.set_footer(text="Cambia al siguiente server save en " + toserversave + ".")
    await ctx.send(embed=embed)



@slash_command(name="tolvl2", description="Experience required for desired level")
@slash_option(
    name="current_lvl",
    description="current Level",
    required=True,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="desired_lvl",
    description="desire Level",
    required=True,
    opt_type=OptionType.INTEGER
)

async def to_lvl_function(ctx: SlashContext, current_lvl: int, desired_lvl: int):
    
    if current_lvl >= desired_lvl:
        await ctx.send("**Warning:** The current level must be lower than the desired level.")
    
    else:
        exp_required = calculate_exp(current_lvl, desired_lvl)    
        await ctx.send(exp_required)
    




######TEST CON COMANDOS






#Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")