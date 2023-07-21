from datetime import datetime
from pytz import utc
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, IntervalTrigger, TimeTrigger, Task


bot = Client(intents=Intents.DEFAULT)
id_channel_publico = 793316701155885056 #Buntar_Publico
role_id = "799964530301992961"  #Buntar
role_buntar = f"<@&{role_id}>"


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



@Task.create(TimeTrigger(hour=18, minute=40))
async def midnight():
    global id_channel_publico
    channel = bot.get_channel(id_channel_publico) # Obtiene el objeto TextChannel
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

@listen()
async def on_ready():
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))
    print("Ready_Last")
    midnight.start()
    
    #Token 
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")