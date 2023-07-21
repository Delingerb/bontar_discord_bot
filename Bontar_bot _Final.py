import math
import pytz
import random
import requests
import pandas as pd
from pytz import utc
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger
from interactions import SlashCommandOption
from interactions.ext.paginators import Paginator

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
async def get_worlds():
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

##serversave
@slash_command(name="ss", description="Next server save")
async def toservers(ctx: SlashContext):
    await ctx.send("Time remaining for the next server save: " + serversave_time + ".")
##serversave

##DROME
@slash_command(name="drome", description="Tibiadrome Rotation")
async def tibiadrome(ctx: SlashContext):
    embed = Embed(title="Tibia Drome",
                url="https://tibia.fandom.com/wiki/Tibiadrome#Rewards",
                description="**NEXT**:\nNext rotation in " + next_drome + ".\n**Reward**:\nSpecial potions, Mount and Outfit points.",
                color="#ffffff")
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/tibia/images/f/f9/Outfit_Lion_of_War_Female_Addon_3.gif/revision/latest?cb=20190522035213&path-prefix=en&format=original")
    await ctx.send(embed=embed)
##DROME

##TEAMTIME
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
##TEAMTIME

##TOLVL
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
##serverinfo

##TOLVL
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
##TOLVL

##SHARE
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
##SHARE

##RASHID
def rashid_message():
    day_of_week = datetime.now().strftime("%A")
    rashid_monday = f"On Mondays you can find him in Svargrond\n in Dankwart's tavern, south of the temple."
    rashid_tuesday = f"On Tuesdays you can find him in Liberty Bay\n in Lyonel's tavern, west of the depot."
    rashid_wednesday = f"On Wednesdays you can find him in Port Hope\n in Clyde's tavern, west of the depot."
    rashid_thursday = f"On Thursdays you can find him in Ankrahmun\n in Arito's tavern, above the post office."
    rashid_friday = f"On Fridays you can find him in Darashia,\n in Miraia's tavern, south of the guildhalls."
    rashid_saturday = f"On Saturdays you can find him in Edron\n in Mirabell's tavern, above the depot."
    rashid_sunday = f"On Sundays you can find him in Carlin depot\n one floor above."

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

@Task.create(TimeTrigger(hour=6, minute=0))
async def midnight():
    rashid_msg = rashid_message()
    global public_channel_id
    channel = bot.get_channel(public_channel_id) # Obtiene el objeto TextChannel
    embed = Embed(title="Rashid",
                url="https://tibia.fandom.com/wiki/Rashid",
                description=rashid_msg,
                color="#00FF00") #verde
    embed.set_thumbnail(url= "https://tibiapal.com/images/Rashid.gif")
    embed.set_image(url="https://cdn.discordapp.com/attachments/743530360780095700/1131302185158852618/Rashid-map.png")
    await channel.send(embed=embed)
    

@slash_command(name="rashid", description="Where is Rashid?")
async def rashid(ctx: SlashContext):
    rashid_msg = rashid_message()
    embed = Embed(title="Rashid",
                url="https://tibia.fandom.com/wiki/Rashid",
                description=rashid_msg,
                color="#00FF00") #verde
    embed.set_thumbnail(url= "https://tibiapal.com/images/Rashid.gif")
    embed.set_image(url="https://cdn.discordapp.com/attachments/743530360780095700/1131302185158852618/Rashid-map.png")
    await ctx.send(embed=embed)
    ##RASHID//

##BOSSES RAROS
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
##RARE BOSSES


####IMBUE/
df = pd.read_excel('imbue_data.xlsx')
wiki_base_url = "https://tibia.fandom.com/wiki/"
wiki_icon="https://static.wikia.nocookie.net/tibia/images/6/6e/TibiaWiki.gif/revision/latest/thumbnail/width/360/height/360?cb=20150121085821&path-prefix=en"
# Obtener los nombres del DataFrame en el orden requerido
desired_order = ['Critical Hit', 'Mana Leech', 'Life Leech', 'Magic Level', 
                'Capacity', 'Axe Fighting', 'Sword Fighting', 'Club Fighting', 
                'Distance Fighting', 'Paralysis Deflection', 'Death Protection', 
                'Earth Protection', 'Fire Protection', 'Ice Protection', 
                'Energy Protection','Holy Protection', 'Fire Damage', 'Earth Damage', 
                'Ice Damage', 'Energy Damage', 'Death Damage', 'Walking Speed', 'Shielding']
sorted_names = sorted(df['Name'], key=lambda x: desired_order.index(x) if x in desired_order else len(desired_order))

@slash_command(name="imbue", description="imbue options",
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
####IMBUE///

#######STAMINA
def stamina_calculator(current_stamina_str, desired_stamina_str):
    def minutes_to_hhmm(minutes):
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        minutes = minutes % 60

        if days > 0:
            return f"{days} day(s) {hours:02d}:{minutes:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}"

    def hhmm_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    regen_point_str = "39:00"  # Hora verde en formato hh:mm
    regen_point = hhmm_to_minutes(regen_point_str)

    current_stamina = hhmm_to_minutes(current_stamina_str)
    desired_stamina = hhmm_to_minutes(desired_stamina_str)

    # Calcular el tiempo de regeneración
    if desired_stamina <= regen_point:
        time_to_regen = (regen_point - current_stamina) * 3 + 10
    else:
        time_to_regen = (regen_point - current_stamina) * 3 + (desired_stamina - regen_point) * 6 + 10
    
    time_to_regen_formatted = minutes_to_hhmm(time_to_regen)
    return time_to_regen_formatted

@slash_command(name="stamina", description="time required for desired level")
@slash_option(
    name="current_hour",
    description="Stamina now",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=41
    )
@slash_option(
    name="current_min",
    description="Stamina now",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=59   
    )
@slash_option(
    name="desired_hour",
    description="Desired Stamina",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=1,
    max_value=42
    )
@slash_option(
    name="desired_min",
    description="Desired Stamina",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=59
    )
async def stamina(ctx: SlashContext, current_hour: int, current_min: int, desired_hour: int, desired_min: int):
    if ((current_hour * 60) + current_min) >= ((desired_hour * 60) + desired_min):
        await ctx.send("**Warning:** The current stamina must be lower than the desired level.")
    elif ((desired_hour * 60) + desired_min) > 2520:
        await ctx.send("**Warning:** stamina cannot be greater than 42:00")
    else:
        waiting_time = stamina_calculator(f"{current_hour}:{current_min}", f"{desired_hour}:{desired_min}")
        current_stamina = f"{current_hour:02d}:{current_min:02d}"
        desired_stamina = f"{desired_hour:02d}:{desired_min:02d}"
        await ctx.send(f"From **{current_stamina}** to  **{desired_stamina}**\nYou need to be offline **{waiting_time}**12.")
#######STAMINA


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