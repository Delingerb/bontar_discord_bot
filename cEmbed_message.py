@slash_command(name="hello", description="My first command :)")
async def hello_test(ctx: SlashContext):
    await ctx.send("Hello, how are you?")

@slash_command(name="boss", description="Boss Boosted of the day.")
async def boss(ctx: SlashContext):
    embed = Embed(title=boss_name,
                  url="https://tibia.fandom.com/wiki/" + boss_name.replace(" ", "_"),
                  description="**Health**: " + hp_value + "\n" + " **Experience**: " + exp_value,
                  color="#ffffff")
    embed.set_thumbnail(url=boss_img)
    embed.set_footer(text="Next server save in " + serversave_time + ".")
    await ctx.send(embed=embed)