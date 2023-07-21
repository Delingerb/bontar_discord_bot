from interactions import Client, Intents, listen,Task, TimeTrigger, IntervalTrigger

bot = Client(intents=Intents.DEFAULT)


counter = 0
@Task.create(IntervalTrigger(seconds=20))
async def print_every_ten():
    global counter  
    counter += 1  
    print(f"Lap {counter}")


##mensaje a canal determinado

@Task.create(TimeTrigger(hour=7, minute=55, utc=False))
async def midnight():
    channel_id = 793316701155885056 #Buntar_Publico
    channel = bot.get_channel(channel_id)  # Obtiene el objeto TextChannel
    await channel.send("Buenos dias @buntar")
    print("It's midnight!")
    

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready_Last")
    print(f"This bot is owned by {bot.owner}")
    midnight.start()

#Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")