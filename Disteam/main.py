import datetime
import discord
import utils
from constants import EMOJIS, TOKEN
from discord.ext import commands
from discord.ext.commands import Context

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    game = discord.Game(f"{len(bot.guilds)} 서버 / {len(bot.users)} 유저")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def recentgame(ctx: Context):
    if ctx.author.bot:
        return

    if utils.isUrl(ctx.message.content.split()[1]):
        user_id = utils.getSteamIDbyURL(ctx.message.content.split()[1])
        if user_id == None:
            embed = utils.getErrorEmbed("해당 유저를 찾을 수 없습니다.")
            await ctx.send(embed=embed)
            return
    else:
        user_id = ctx.message.content.split()[1]

    loading_message = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    profile = utils.getUserInfo(user_id)

    if profile == 0:
        embed = utils.getErrorEmbed("해당 유저를 찾을 수 없습니다.")
        await ctx.send(embed=embed)
        await loading_message.delete()
        return

    embed = discord.Embed(
        title=profile["personaname"],
        description="님의 최근 게임 목록",
        url="https://steamcommunity.com/profiles/{0}".format(user_id),
    )
    embed.set_thumbnail(url=profile["avatarfull"])
    await ctx.send(embed=embed)

    games = utils.getRecentGames(user_id)

    if games == 0:
        embed = utils.getErrorEmbed("최근 게임 목록을 불러올 수 없습니다.")
        await ctx.send(embed=embed)
        await loading_message.delete()
        return

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


@bot.command()
async def ping(ctx: Context):
    if ctx.author.bot:
        return

    await ctx.send(f"{round(bot.latency * 1000)}ms")


@bot.command()
async def profile(ctx: Context):
    if ctx.author.bot:
        return

    if utils.isUrl(ctx.message.content.split()[1]):
        user_id = utils.getSteamIDbyURL(ctx.message.content.split()[1])
        if user_id == None:
            embed = utils.getErrorEmbed("해당 유저를 찾을 수 없습니다.")
            await ctx.send(embed=embed)
            return
    else:
        user_id = ctx.message.content.split()[1]

    loading_message = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    profile = utils.getUserInfo(user_id)

    if profile == 0:
        embed = utils.getErrorEmbed("해당 유저를 찾을 수 없습니다.")
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title=profile["personaname"],
        url="https://steamcommunity.com/profiles/{0}".format(user_id),
    )

    embed.add_field(name="ID", value=user_id, inline=False)

    country = profile.get("loccountrycode")
    if country:
        embed.add_field(name="Country", value=country, inline=False)

    level = utils.getUserLevel(user_id)
    if not (level == 0 or level == 1):
        embed.add_field(name="Level", value=level, inline=False)

    time_created_unixtime = profile.get("timecreated")
    if time_created_unixtime:
        time_created = datetime.datetime.utcfromtimestamp(
            time_created_unixtime
        ).strftime("%Y %m %d")
        embed.add_field(name="Account Create Time", value=time_created, inline=False)

    game_count = utils.getUserOwnedGameCount(user_id)
    if not (game_count == 0 or game_count == 1):
        embed.add_field(name="Game Count", value=game_count, inline=False)

    embed.set_thumbnail(url=profile["avatarfull"])

    embed.set_footer(text="스팀 프로필 공개 범위 설정에 따라 결과가 달라질 수 있습니다.")

    await loading_message.delete()

    await ctx.send(embed=embed)


bot.run(TOKEN)
