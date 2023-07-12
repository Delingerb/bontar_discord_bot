from interactions import Client, Intents, listen, OptionType, slash_command, SlashContext, slash_option
import requests

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="hola", description="My first command :)")
async def my_hello(ctx: SlashContext):
    await ctx.send("Hello, ¿todo bien?")

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

@slash_command(name="world5", description="Server Info")
@slash_option(
    name="server_opt",
    description="String Option",
    required=True,
    opt_type=OptionType.STRING
)
async def my_command_function(ctx: SlashContext, server_opt: str):
    server_opt_capitalized = server_opt.capitalize()  # Convertir la primera letra a mayúscula

    world_info = get_world_info(server_opt_capitalized)

    if world_info and world_info.get('name') == server_opt_capitalized:
        name = world_info['name']
        status = world_info['status']
        players_online = world_info['players_online']
        
        await ctx.send(f"World Name: {name}\nStatus: {status}\nPlayers online: {players_online}")
    else:
        await ctx.send(f"Failed to fetch data for the world '{server_opt_capitalized}'.")



bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")
