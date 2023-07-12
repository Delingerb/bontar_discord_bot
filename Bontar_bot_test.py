from interactions import Client, Intents, listen, OptionType, slash_command, SlashContext, slash_option
import requests



bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="hola", description="My first command :)")
async def my_hello(ctx: SlashContext):
    await ctx.send("Hello todo bien?")

# TESTING
import requests

def get_world_info(world_name):
    url = f'https://api.tibiadata.com/v3/world/{world_name.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        worlds = data['worlds']
        world_info = worlds['world']
        
        return world_info
    else:
        return None


world_name = 'Solidera'
world_info = get_world_info(world_name)

# Verificar si la obtención de información fue exitosa
if world_info:
    # Guardar cada categoría en una variable
    name = world_info['name']
    status = world_info['status']
    players_online = world_info['players_online']
    record_players = world_info['record_players']
    record_date = world_info['record_date']
    creation_date = world_info['creation_date']
    location = world_info['location']
    pvp_type = world_info['pvp_type']
    premium_only = world_info['premium_only']
    transfer_type = world_info['transfer_type']
    world_quest_titles = world_info['world_quest_titles']
    battleye_protected = world_info['battleye_protected']
    battleye_date = world_info['battleye_date']
    game_world_type = world_info['game_world_type']
    tournament_world_type = world_info['tournament_world_type']
    online_players = world_info['online_players']
    
    # Imprimir lista de jugadores en línea
    #print("Online Players:")
    #for player in online_players:
        #player_name = player['name']
        #player_level = player['level']
        #player_vocation = player['vocation']
        #print(f"- Name: {player_name}, Level: {player_level}, Vocation: {player_vocation}")
else:
    print(f"Failed to fetch data for the world '{world_name}'.")



####SLASH COMANDO



@slash_command(name="world",description="Server Info")
@slash_option(
    name="server_opt",
    description="String Option",
    required=True,
    opt_type=OptionType.STRING
)
async def my_command_function(ctx: SlashContext, server_opt: str):
    world_info = get_world_info(server_opt)

    if world_info:
        name = world_info['name']
        status = world_info['status']
        players_online = world_info['players_online']
        record_players = world_info['record_players']
        record_date = world_info['record_date']
        creation_date = world_info['creation_date']
        location = world_info['location']
        pvp_type = world_info['pvp_type']
        premium_only = world_info['premium_only']
        transfer_type = world_info['transfer_type']
        world_quest_titles = world_info['world_quest_titles']
        battleye_protected = world_info['battleye_protected']
        battleye_date = world_info['battleye_date']
        game_world_type = world_info['game_world_type']
        
        await ctx.send(f"World Name: {name}\nStatus: {status}\nPlayers_online: {players_online}")
    else:
        await ctx.send(f"Failed to fetch data for the world '{world_name}'.")

    
    
    
    
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")