from twitchio.ext import commands


@commands.command(name='joingame')
async def create_player(ctx: commands.Context):
    await ctx.send(f"{ctx.author.name}, Bienvenue dans l'aventure")
    name = ctx.author.name
    return name
