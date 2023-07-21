from pytz import utc
from datetime import datetime, timedelta
from interactions import Client, Intents, listen, Embed, slash_command, SlashContext, slash_option, OptionType, Task, TimeTrigger
from interactions import SlashCommandOption, SlashCommandChoice
from interactions import ActionRow, Button, ButtonStyle, ComponentCommand, ComponentType, ComponentContext, component_callback
from interactions import ActionRow, Button, spread_to_rows, StringSelectMenu, StringSelectOption
from interactions.api.events import Component

bot = Client(intents=Intents.DEFAULT)

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

@slash_command(name="imbue_button", description="My first command :)")
async def imbue_button(ctx: SlashContext):
    components = spread_to_rows(
        Button(
            custom_id="common_id",
            style=ButtonStyle.BLUE,
            label="Common",
        ),
        Button(
            custom_id="defence_id",
            style=ButtonStyle.GREEN,
            label="Defence",
        ),
        Button(
            custom_id="skill_id",
            style=ButtonStyle.GREY,
            label="Skill",
        ),
        Button(
            custom_id="attack_id",
            style=ButtonStyle.RED,
            label="Attack",
        ),
        StringSelectMenu(
            StringSelectOption(
                label="Vanilla",
                value="vanilla"
            ),
            StringSelectOption(
                label="Chocolate",
                value="chocolate"
            ),
            StringSelectOption(
                label="Strawberry",
                value="strawberry"
            ),
            StringSelectOption(
                label="Mint",
                value="mint"
            ),
            StringSelectOption(
                label="Caramel",
                value="caramel"
            ),
            placeholder="Choose your imbue",
            custom_id="type_imbue",
            min_values=1,
            max_values=1,
        )
    )
    
    embed = Embed(
        title="Imbue Name",
        url="https://tibia.fandom.com/wiki/",
        description="DATA DATA DATA DATA DATA DATA",
        color="#ffffff"
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/tibia/images/c/cf/Basic_Venom.png/revision/latest?cb=20171026202704&path-prefix=en&format=original")
    embed.set_footer(text="probando todas las opciones")
    
    await ctx.send(embed=embed, components=components)

@listen()
async def on_component(event: Component):
    ctx = event.ctx

    match ctx.custom_id:
        case "common_id":
            await ctx.send("You clicked it!")
        case "defence_id":
            await ctx.send("You clicked defence!")
        case "attack_id":
            await ctx.send("You clicked attack!")
        case "skill_id":
            await ctx.send("You clicked skill!")
        case "type_imbue":
            option = ctx.values[0]
            await ctx.send(f"type_imbue {option}")



@listen()
async def on_ready():
    print("Ready papá")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))

bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")
