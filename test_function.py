from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, IntervalTrigger, TimeTrigger, Task

bot = Client(intents=Intents.DEFAULT)
id_channel_publico = 793316701155885056 #Buntar_Publico
role_id = "799964530301992961"  #Buntar
role_buntar = f"<@&{role_id}>"



@listen()
async def on_ready():
    print(datetime.now().strftime("%H:%M:%S"))
    print("Ready_Last")
    

# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")