import math
import pytz
from pytz import utc
import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger

bot = Client(intents=Intents.DEFAULT)
public_channel_id = 793316701155885056  # Buntar_public
role_id = "799964530301992961"  # Buntar
role_buntar = f"<@&{role_id}>"

api = "https://api.tibiadata.com/v3/"

# FUNCTIONS //////

# SCHEDULES
def get_time(country):
    try:
        time_zone = pytz.timezone(country)
        current_time = datetime.now(tz=time_zone)
        return current_time.strftime('%H:%M')
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Time zone not found for {country}")

argentina_time = get_time('America/Buenos_Aires')  
chile_time = get_time('America/Santiago')
ecuador_time = get_time('America/Guayaquil')
mexico_time = get_time('America/Mexico_City')
usa_time1 = get_time('America/New_York') 
spain_time = get_time('Europe/Madrid') 
# SCHEDULES /

# BOSS BOOSTED
# Get the HTML content of the web page
wikiurl = "https://tibia.fandom.com/wiki/Main_Page"
response = requests.get(wikiurl)
html_content = response.text

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")
# Find the element with the class "compact-box compact-box-boss no-pseudoelements-container"
element = soup.find("div", class_="compact-box compact-box-boss no-pseudoelements-container")
# Get the boss name
boss_name = element.find("b").text.strip()
# HP **************
hp_span = element.find("span", class_="creature-stats-hp")
hp_value = hp_span.find("span", class_="tibiatext").text
# Exp******************
exp_span = element.find("span", class_="creature-stats-exp")
exp_value = exp_span.find("span", class_="tibiatext").text
# Get Image ******************
image_span = element.find("span", class_="no-pseudoelements-container")
boss_img = image_span.find("img")["data-src"]
# BOSS BOOSTED /

# SERVER SAVE
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
serversave_time = f"{remaining_hours:02d}:{remaining_minutes:02d}"
# SERVER SAVE /

# TIBIADROME
# Definir la fecha objetivo para un miércoles específico
target_date = datetime(2023, 7, 26, 8, 0)
current_date = datetime.utcnow()
remaining_time = target_date - current_date

if remaining_time.total_seconds() <= 0:
    target_date += timedelta(days=14)
    remaining_time = target_date - current_date

days = remaining_time.days
remaining_hours, remaining_seconds = divmod(remaining_time.seconds, 3600)
remaining_minutes = remaining_seconds // 60

next_drome = f"{days} days {remaining_hours:02d}:{remaining_minutes:02d}"
# TIBIADROME /

## SERVER_INFO
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
## SERVER_INFO /



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

    message = f"A level **{user_level}** can share experience with levels **{minimum_level}** to **{maximum_level}**."
    return message
##PARTY_SHARE/






@slash_command(name="hello", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

@slash_command(name="boss", description="Boss Boosted of the day.")
async def boss(ctx: SlashContext):
    embed = Embed(title=boss_name,
                  url="https://tibia.fandom.com/wiki/" + boss_name.replace(" ", "_"),
                  description="**Health**: " + hp_value + "\n" + " **Experience**: " + exp_value,
                  color="#ffffff")
    embed.set_thumbnail(url=boss_img)
    embed.set_footer(text="Next server save in " + serversave_time + ".")
    await ctx.send(embed=embed)

@slash_command(name="ss", description="Next server save")
async def toservers(ctx: SlashContext):
    await ctx.send("Time remaining for the next server save: " + serversave_time + ".")

@slash_command(name="drome", description="Tibiadrome Rotation")
async def tibiadrome(ctx: SlashContext):
    embed = Embed(title="Tibia Drome",
                  url="https://tibia.fandom.com/wiki/Tibiadrome#Rewards",
                  description="**NEXT**:\nNext rotation in " + next_drome + ".\n**Reward**:\nSpecial potions, Mount and Outfit points.",
                  color="#ffffff")
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/tibia/images/f/f9/Outfit_Lion_of_War_Female_Addon_3.gif/revision/latest?cb=20190522035213&path-prefix=en&format=original")
    await ctx.send(embed=embed)

@slash_command(name="hours", description="Team Schedule")
async def hours(ctx: SlashContext):
    embed = Embed(title="Team Schedule",
                  description="**Schedules:**\n" +
                              "Madrid: " + spain_time + "\n" +
                              "Argentina/Brazil: " + argentina_time + "\n" +
                              "Santiago/Darki/Vzla: " + chile_time + "\n" +
                              "Peru/Ecuador/Colombia/Victor: " + ecuador_time + "\n" +
                              "Gonzalo: " + mexico_time,
                  color="#ffffff")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/745374445668925591/1128011098596053104/f.elconfidencial.com_original_a39_499_f1e_a39499f1e51ddf3af7fc8b4a0756195a.jpg")
    await ctx.send(embed=embed)

@slash_command(name="world", description="Server Info")
@slash_option(
    name="server_opt",
    description="Check server",
    required=True,
    opt_type=OptionType.STRING
)
async def world_info(ctx: SlashContext, server_opt: str):
    server_opt_capitalized = server_opt.capitalize()  # Convert the first letter to uppercase

    world_info = get_world_info(server_opt_capitalized)

    if world_info and world_info.get('name') == server_opt_capitalized:
        name = world_info['name']
        status = world_info['status']
        players_online = world_info['players_online']
        location = world_info['location']
        pvp_type = world_info['pvp_type']

        await ctx.send(f"World Name: **{name}**\nType: {pvp_type}\nStatus: {status}\nLocation: {location}\nPlayers online: {players_online}")
    else:
        await ctx.send(f"**Wrong server name '{server_opt_capitalized}'.**")



@slash_command(name="tolvl", description="Experience required for desired level")
@slash_option(
    name="current_lvl",
    description="Current Level",
    required=True,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="desired_lvl",
    description="Desired Level",
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
    description="Current Level",
    required=True,
    opt_type=OptionType.INTEGER
)
async def share_lvl_function(ctx: SlashContext, level: int):
    
        party_result = party_share(level)    
        await ctx.send(party_result)


def rashid_message():
    day_of_week = datetime.now().strftime("%A")

    rashid_monday = f"On Mondays you can find him in **Svargrond**\n in Dankwart's tavern, south of the temple."
    rashid_tuesday = f"On Tuesdays you can find him in **Liberty Bay**\n in Lyonel's tavern, west of the depot."
    rashid_wednesday = f"On Wednesdays you can find him in **Port Hope**\n in Clyde's tavern, west of the depot."
    rashid_thursday = f"On Thursdays you can find him in **Ankrahmun**\n in Arito's tavern, above the post office."
    rashid_friday = f"On Fridays you can find him in **Darashia**\n in Miraia's tavern, south of the guildhalls."
    rashid_saturday = f"On Saturdays you can find him in **Edron**\n in Mirabell's tavern, above the depot."
    rashid_sunday = f"On Sundays you can find him in **Carlin** depot\n one floor above."

    if day_of_week == "Monday":
        return rashid_monday
    elif day_of_week == "Tuesday":
        return rashid_tuesday
    elif day_of_week == "Wednesday":
        return rashid_wednesday
    elif day_of_week == "Thursday":
        return rashid_thursday
    elif day_of_week == "Friday":
        return rashid_friday
    elif day_of_week == "Saturday":
        return rashid_saturday
    elif day_of_week == "Sunday":
        return rashid_sunday
    else:
        return "Invalid day. Please provide a valid day of the week."


@Task.create(TimeTrigger(hour=10, minute=0, utc=False))
async def midnight():
    global public_channel_id
    channel = bot.get_channel(public_channel_id)  # Get the TextChannel object
    
    rashid_day = rashid_message()

    embed = Embed(title="Rashid",
                url="https://tibia.fandom.com/wiki/Rashid",
                description=rashid_day,
                color="#00FF00") #green
    embed.set_thumbnail(url="https://tibiapal.com/images/Rashid.gif")
    await channel.send(embed=embed)
    print("It's midnight!")


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
    data = data.drop(['Type', 'Introduced', 'Expected in', 'Killed bosses', 'Killed players', 'Last seen', '#', 'Image'], axis=1)
    data = data[~data['Boss name'].isin(not_wanted)]
    pattern = r'^\d+(\.\d+)?%'
    data = data[data['Possibility'].str.extract(pattern, expand=False).notnull()]
    data['Possibility'] = data['Possibility'].str.rstrip('%')
    data['Possibility'] = data['Possibility'].astype('float64')

    filtered_data = data[data['Possibility'] >= 16]
    
    # Crear una copia explícita del DataFrame
    data_copy = filtered_data.copy()
        
    # Agregar una columna "Image URL" a la copia
    data_copy['Image URL'] = data_copy['Boss name'].str.replace(' ', '_', regex=True)
    data_copy['Image URL'] = "https://guildstats.eu/images/bosses/" + data_copy['Image URL'] + ".gif"
    # Agregar una columna "wiki" a la copia
    data_copy['wiki URL'] = "https://tibia.fandom.com/wiki/" + data_copy['Boss name']
    data_copy['wiki URL'] = data_copy['wiki URL'].str.replace(' ', '_', regex=True)
    
    # Modificar la columna "Boss name" en la copia
    #data_copy.loc[:, 'Boss name'] = data_copy['Boss name'].str.capitalize()
        
    sorted_data = data_copy.sort_values('Possibility', ascending=False)

    return sorted_data
    
@slash_command(name="rare_bosses", description="Probability of rare bosses of the day")
async def boss_command(ctx: SlashContext):
    # Obtener los datos filtrados
    filtered_data = rare_bosses()

    # Enviar un embed para cada jefe
    for _, row in filtered_data.iterrows():
        boss_name = row['Boss name']
        possibility = row['Possibility']
        image_url = row['Image URL']
        wiki_url = row['wiki URL']

        # Crear un embed para el jefe actual
        embed = Embed(title=boss_name, description=f"Probability: {possibility}%", color=random.randint(0, 0xFFFFFF), url=wiki_url)
        embed.set_thumbnail(url=image_url)

        await ctx.send(embed=embed)


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready_Last")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))
    midnight.start()

#Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")
