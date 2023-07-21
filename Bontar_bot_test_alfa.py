import math
import pytz
from pytz import utc
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from interactions import SlashCommandOption, SlashCommandChoice
import re

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")
    
#############################

def stamina_calculator(current_stamina_str, desired_stamina_str):
    def minutes_to_hhmm(minutes):
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        minutes = minutes % 60

        if days > 0:
            return f"{days} día(s) {hours:02d}:{minutes:02d}"
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
    opt_type=OptionType.STRING
)
@slash_option(
    name="current_min",
    description="Stamina now",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="desired_hour",
    description="Desired Stamina",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="desired_min",
    description="Desired Stamina",
    required=True,
    opt_type=OptionType.STRING
)
async def stamina(ctx: SlashContext, current_hour: int, current_min: int, desired_hour: int, desired_min: int):
    if ((current_hour*60)+current_min) >= ((desired_hour*60)+desired_min):
        await ctx.send("**Warning:** The current stamina must be lower than the desired level.")
    else:
        waiting_time = stamina_calculator(f"{current_hour}:{current_min}", f"{desired_hour}:{desired_min}")    
        await ctx.send(waiting_time)
    
    
#############################

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready papá")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))

# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")
