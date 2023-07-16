import time
from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType

@listen()  
async def on_ready():
    print("Ready_Last")


@slash_command(name="embed_test", description="embed update")
async def embed_test(ctx: SlashContext):
    embed = {
        "title": "Título actualizado",
        "description": "Descripción actualizada"
    }
    
    mensaje = await ctx.send(embed=embed)  # Envía el mensaje inicial con el embed
    
    while True:
        embed["description"] += " (actualizado1)"
        await mensaje.edit(embed=embed)  # Edita el mensaje con el embed actualizado
        time.sleep(10)  # Espera 5 segundos antes de la próxima actualización
        



###### COPIA CON TIEMPOS DIFERENTES
@slash_command(name="embed_test2", description="embed update")
async def embed_test2(ctx: SlashContext):
    embed = {
        "title": "Título actualizado",
        "description": "Descripción actualizada"
    }
    
    mensaje = await ctx.send(embed=embed)  # Envía el mensaje inicial con el embed
    
    while True:
        embed["description"] += " (actualizado2)"
        await mensaje.edit(embed=embed)  # Edita el mensaje con el embed actualizado
        time.sleep(5)  # Espera 5 segundos antes de la próxima actualización





bot = Client(intents=Intents.DEFAULT)
# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")