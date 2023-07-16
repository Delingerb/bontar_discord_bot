
from interactions import Client, listen, Intents, Task, IntervalTrigger, TimeTrigger

bot = Client(intents=Intents.DEFAULT)

counter = 0

#TO TEST
@Task.create(IntervalTrigger(seconds=20))
async def print_every_ten():
    global counter  
    counter += 1  
    print(f"Lap {counter}")


@Task.create(TimeTrigger(hour=7, minute=55, utc=False))
async def midnight():
    channel_id = 793316701155885056 #Buntar_Publico
    channel = bot.get_channel(channel_id)  # Obtiene el objeto TextChannel
    await channel.send("Buenos dias @buntar")
    print("It's midnight!")




@listen()
async def on_ready():
    print("Ready_Last")
    print_every_ten.start()  
    midnight.start()  

# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")