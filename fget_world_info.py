import requests

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

world_name = 'Adra'  # Nombre del mundo que deseas obtener información
world_info = get_world_info(world_name)

if world_info:
    name = world_info['name']
    status = world_info['status']
    players_online = world_info['players_online']
    location = world_info['location']
    pvp_type = world_info['pvp_type']
    premium_only = world_info['premium_only']
    transfer_type = world_info['transfer_type']
    battleye_protected = world_info['battleye_protected']
    battleye_date = world_info['battleye_date']
    game_world_type = world_info['game_world_type']

    print(f"World Name: {name}")
    print(f"Status: {status}")
    print(f"Players online: {players_online}")
    print(f"Location: {location}")
    print(f"PvP Type: {pvp_type}")
    print(f"Premium Only: {premium_only}")
    print(f"Transfer Type: {transfer_type}")
    print(f"Battleye Protected: {battleye_protected}")
    print(f"Battleye Date: {battleye_date}")
    print(f"Game World Type: {game_world_type}")
else:
    print(f"Failed to fetch data for the world '{world_name}'.")
