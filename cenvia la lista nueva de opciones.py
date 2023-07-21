
from pytz import utc
from datetime import datetime
from interactions import Client, Intents, listen, slash_command, SlashContext
from interactions import ActionRow, Button, ButtonStyle, StringSelectMenu, StringSelectOption
from interactions.api.events import Component

bot = Client(intents=Intents.DEFAULT)

@slash_command(name="hello_test", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

@slash_command(name="imbue_button", description="My first command :)")
async def imbue_button(ctx: SlashContext):
    components = [
        ActionRow(
            Button(
                custom_id="common_id",
                style=ButtonStyle.BLUE,
                label="Common"
            ),
            Button(
                custom_id="defence_id",
                style=ButtonStyle.GREEN,
                label="Defence"
            )
        ),
        ActionRow(
            Button(
                custom_id="skill_id",
                style=ButtonStyle.GREY,
                label="Skill"
            ),
            Button(
                custom_id="attack_id",
                style=ButtonStyle.RED,
                label="Attack"
            )
        )        
    ]

    await ctx.send("Select an option:", components=components)

@listen()
async def on_component(event: Component):
    ctx = event.ctx
    if ctx.custom_id == "common_id":
        components = [
            ActionRow(
                StringSelectMenu(
                    StringSelectOption(
                        label="Option 1",
                        value="option_1"
                    ),
                    StringSelectOption(
                        label="Option 2",
                        value="option_2"
                    ),
                    placeholder="Select an option",
                    custom_id="select_option_common"
                )
            )
        ]
        await ctx.send("Common button clicked", components=components)
    elif ctx.custom_id == "defence_id":
        components = [
            ActionRow(
                StringSelectMenu(
                    StringSelectOption(
                        label="Option 3",
                        value="option_3"
                    ),
                    StringSelectOption(
                        label="Option 4",
                        value="option_4"
                    ),
                    placeholder="Select an option",
                    custom_id="select_option_defence"
                )
            )
        ]
        await ctx.send("Defence button clicked", components=components)
    elif ctx.custom_id == "skill_id":
        components = [
            ActionRow(
                StringSelectMenu(
                    StringSelectOption(
                        label="Option 5",
                        value="option_5"
                    ),
                    StringSelectOption(
                        label="Option 6",
                        value="option_6"
                    ),
                    placeholder="Select an option",
                    custom_id="select_option_skill"
                )
            )
        ]
        await ctx.send("Skill button clicked", components=components)
    elif ctx.custom_id == "attack_id":
        components = [
            ActionRow(
                StringSelectMenu(
                    StringSelectOption(
                        label="Option 7",
                        value="option_7"
                    ),
                    StringSelectOption(
                        label="Option 8",
                        value="option_8"
                    ),
                    placeholder="Select an option",
                    custom_id="select_option_attack"
                )
            )
        ]
        await ctx.send("Attack button clicked", components=components)
    elif ctx.custom_id == "select_option_common":
        selected_option = ctx.values[0]
        await ctx.send(f"Selected option (Common): {selected_option}")
    elif ctx.custom_id == "select_option_defence":
        selected_option = ctx.values[0]
        await ctx.send(f"Selected option (Defence): {selected_option}")
    elif ctx.custom_id == "select_option_skill":
        selected_option = ctx.values[0]
        await ctx.send(f"Selected option (Skill): {selected_option}")
    elif ctx.custom_id == "select_option_attack":
        selected_option = ctx.values[0]
        await ctx.send(f"Selected option (Attack): {selected_option}")

@listen()
async def on_ready():
    print("Ready papá")
    print(f"This bot is owned by {bot.owner}")
    print(datetime.now().strftime("%H:%M:%S"))
    print(datetime.now(utc).strftime("%H:%M:%S"))

bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")
