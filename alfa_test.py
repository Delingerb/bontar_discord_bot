from interactions import Client, Intents, listen,Embed, slash_command, SlashContext, slash_option, OptionType

@listen()  
async def on_ready():
    print("Ready_Last")


@slash_command(name="role", description="prueba mention role3")
async def role_test(ctx: SlashContext):
    role_id = "799964530301992961"  # Reemplaza "ID_DEL_ROL" con el ID del rol objetivo
    role_mention = f"<@&{role_id}>"
    await ctx.send(f"Hello todo bien? {role_mention}")




bot = Client(intents=Intents.DEFAULT)
# Iniciar el bot
bot.start("MTEyNzQzMTk2NDU4MDkyMTM4NQ.Gf2sgN.wKl40sYpfZIRH8Q-PM8gxYWADvzV_vd3KtNkpE")