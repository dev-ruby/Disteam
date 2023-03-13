import discord
from discord.ext import commands
from discord.ext.commands import Context
import utils
from constants import TOKEN, EMOJIS

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command()
async def recentgame(ctx: Context):
    if ctx.author.bot:
        return
    
    user_id = ctx.message.content.split()[1]

    loading_message = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    profile = utils.getUserInfo(user_id)

    profile_embed = discord.Embed(
        title=profile["personaname"],
        description="님의 최근 게임 목록",
        url="https://steamcommunity.com/profiles/{0}".format(user_id),
    )
    profile_embed.set_thumbnail(url=profile["avatarfull"])
    await ctx.send(embed=profile_embed)

    games = utils.getRecentGames(user_id)

    for game in games:
        embed = discord.Embed(
            title=game["name"],
            url="https://store.steampowered.com/app/{0}".format(game["appid"]),
        )
        embed.set_image(
            url="https://cdn.cloudflare.steamstatic.com/steam/apps/{0}/header.jpg".format(
                game["appid"]
            )
        )
        embed.add_field(
            name="전체 플레이타임",
            value="{0}시간{1}분".format(*divmod(game["playtime_forever"], 60)),
            inline=True,
        )
        embed.add_field(
            name="2주 플레이타임",
            value="{0}시간{1}분".format(*divmod(game["playtime_2weeks"], 60)),
            inline=True,
        )
        await ctx.send(embed=embed)

    await loading_message.delete()


bot.run(TOKEN)