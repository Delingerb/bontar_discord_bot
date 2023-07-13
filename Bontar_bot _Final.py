import math
import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType


bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

api = "https://docs.tibiadata.com/"



# FUNCIONES //////

#HORARIOS
def obtener_hora(pais):
    try:
        zona_horaria = pytz.timezone(pais)
        hora_actual = datetime.now(tz=zona_horaria)
        return hora_actual.strftime('%H:%M')
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"No se encontró la zona horaria para {pais}")

hora_arg = obtener_hora('America/Buenos_Aires')  
hora_chile = obtener_hora('America/Santiago')
hora_ecuador = obtener_hora('America/Guayaquil')
hora_mex = obtener_hora('America/Mexico_City')
hora_usa1 = obtener_hora('America/New_York') 
hora_espana = obtener_hora('Europe/Madrid') 
#HORARIOS/



#BOSS BOSSTED
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
    #BOSSBOSTED /

#SERVERSAVE
current_time = datetime.utcnow()
# Create a time object for 10:00 a.m. in UTC (8:00 a.m. in CEST)
target_time = datetime(current_time.year, current_time.month, current_time.day, 8, 0, 0)
# Set the target time for the next day if it has already passed
if current_time.hour >= 8:
    target_time = target_time + timedelta(days=1)
# Calculate the remaining time in seconds
time_remaining = target_time - current_time
remaining_seconds = time_remaining.total_seconds()
# Calculate the remaining hours and minutes
remaining_hours = int(remaining_seconds // 3600)
remaining_minutes = int((remaining_seconds % 3600) // 60)

# Format the result in hh:mm format
toserversave = f"{remaining_hours:02d}:{remaining_minutes:02d}"
#SERVERSAVE/

#TIBIADROME
current_date = datetime.utcnow()
remaining_days = (2 - current_date.weekday()) % 14
target_date = current_date + timedelta(days=remaining_days)
target_date = target_date.replace(hour=8, minute=0, second=0, microsecond=0)
remaining_time = target_date - current_date
days = remaining_time.days
remaining_hours, remaining_seconds = divmod(remaining_time.seconds, 3600)
remaining_minutes = remaining_seconds // 60
if remaining_time.total_seconds() < 0:
    days += 7
time_drome_left = f"{days} days {remaining_hours:02d}:{remaining_minutes:02d}"
#TIBIADROME/


##SERVER_INFO
def get_worlds():
    url = 'https://api.tibiadata.com/v3/worlds'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        worlds = data['worlds']['regular_worlds']
        return worlds
    else:
        return None

def get_world_info(world_name):
    worlds = get_worlds()

    if worlds:
        for world in worlds:
            if world['name'].lower() == world_name.lower():
                return world
    
    return None
##SERVER_INFO/


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

##PARTY_SHARE
def party_share(user_level):
    minimum_level = math.ceil(user_level * (2/3))
    maximum_level = math.ceil(user_level * (3/2))

    message = f"A level {user_level} can share experience with levels {minimum_level} to {maximum_level}."
    return message
##PARTY_SHARE/






@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready_Last")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="hola", description="My first command :)")
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

@slash_command(name="ss", description="Proximo server save")
async def toservers(ctx: SlashContext):
    await ctx.send("faltan "+ toserversave + " para el Server Save.")

@slash_command(name="drome", description="Rotación Tibia Drome")
async def tibiadrome(ctx:SlashContext):
    embed = Embed(title= "Tibia Drome",
                url="https://tibia.fandom.com/wiki/Tibiadrome#Rewards",
                description= "**NEXT**:" + "\n" +"Siguiente rotación en " + time_drome_left + "." + "\n" + "**Reward**:" + "\n" + "Potions especiales, puntos para Mount y Outfit",
                color="#ffffff")
    embed.set_thumbnail(url= "https://static.wikia.nocookie.net/tibia/images/f/f9/Outfit_Lion_of_War_Female_Addon_3.gif/revision/latest?cb=20190522035213&path-prefix=en&format=original")
    await ctx.send(embed=embed)


@slash_command(name="horas", description="Horas del team")
async def horas(ctx:SlashContext):
    embed = Embed(title= "Horarios del team",
                  description= "**Horarios: **" + "\n" + 
                  "Madrid: " + hora_espana + "\n" +
                  "Argentina/Brasil: " + hora_arg + "\n" + 
                  "Santiago/Darki/Vzla: " + hora_chile + "\n" +  
                  "Peru/Ecuardor/Col/Victor: " + hora_ecuador + "\n" + 
                  "Gonzalo: " + hora_mex,
                  color="#ffffff")
    embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/745374445668925591/1128011098596053104/f.elconfidencial.com_original_a39_499_f1e_a39499f1e51ddf3af7fc8b4a0756195a.jpg")
    await ctx.send(embed=embed)
    
    
    
@slash_command(name="world", description="Server Info")
@slash_option(
    name="server_opt",
    description="String Option",
    required=True,
    opt_type=OptionType.STRING
)
async def world_info(ctx: SlashContext, server_opt: str):
    server_opt_capitalized = server_opt.capitalize()  # Convertir la primera letra a mayúscula

    world_info = get_world_info(server_opt_capitalized)

    if world_info and world_info.get('name') == server_opt_capitalized:
        name = world_info['name']
        status = world_info['status']
        players_online = world_info['players_online']
        location = world_info['location']
        pvp_type = world_info['pvp_type']
        
        await ctx.send(f"World Name: {name}\nPVP: {pvp_type}\nStatus: {status}\nLocation: {location}\nPlayers online: {players_online}")
    else:
        await ctx.send(f"Failed to fetch data for the world '{server_opt_capitalized}'.")


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
    

@slash_command(name="share", description="Party Share")
@slash_option(
    name="level",
    description="current Level",
    required=True,
    opt_type=OptionType.INTEGER
)

async def share_lvl_function(ctx: SlashContext, level: int):
    
        party_result = party_share(level)    
        await ctx.send(party_result)



#Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")