import os
import discord
import requests
import interactions
from lxml import etree
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

bot = discord.Client(intents=discord.Intents.DEFAULT)
slash = SlashCommand(bot, sync_commands=True)
token = "MTEyNzQxNTE4NzMxMDM5MTM2Nw.GCz-PA.6fteJet2XkgTPd79DlplGyRGnsmmpudwt10Ew8"

api = "https://docs.tibiadata.com/"

@bot.event
async def on_ready():
    print('Bot conectado como {0.user}'.format(bot))

@slash.slash(name="testpy", description="My first command :)")
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")

@slash.slash(
    name="embedtest",
    description="For testing",
)
async def ping(ctx: SlashContext):
    # Realizar web scraping para obtener la URL del GIF
    url = "https://www.tibiawiki.com.br/"  # Reemplaza con la URL de la página que se actualiza diariamente
    response = requests.get(url)
    html_content = response.text
    gif_xpth = "/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[3]/div/div[2]/div/div/a/img"
    tree = etree.HTML(html_content)
    gif_element = tree.xpath(gif_xpth)  # Ajusta el XPath de acuerdo a la estructura HTML de la página
    gif_url = gif_element[0].get("src") if gif_element else None

    embed = discord.Embed(
        title="Your title",
        url="https://google.com",
        description="Your description",
        color=discord.Color.white()
    )
    
    embed.set_image(url=gif_url)  # Agregar el GIF al embed
    await ctx.send(embed=embed)


bot.start(os.environ['TOKEN'])
