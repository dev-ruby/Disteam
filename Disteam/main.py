import datetime
import discord
from constants import EMOJIS, TOKEN
from discord.ext import commands
from discord.ext.commands import Context

from uri import URI
from steam_game import SteamGame
from steam_profile import SteamProfile
from steam_user import SteamUser

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)


def getErrorEmbed(desc: str) -> discord.Embed:
    return discord.Embed(
        title=":no_entry: Error",
        description=desc,
        color=0xFF0000
    )


@bot.event
async def on_ready():
    game = discord.Game(f"{len(bot.guilds)} 서버 / {len(bot.users)} 유저")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def recentgame(ctx: Context) -> None:
    if ctx.author.bot:
        return

    ldmsg = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    try:

        url: URI = URI(ctx.message.content.split()[1])
        user: SteamUser = SteamUser.query_user(
            url) if url.is_valid() else SteamUser(url.to_string())
        if user == None:
            embed = getErrorEmbed("해당 유저를 찾을 수 없습니다.")
            await ctx.send(embed=embed)
            return

        profile: SteamProfile = user.get_profile()
        if profile == None:
            embed = getErrorEmbed("프로필을 불러오지 못했습니다.")
            await ctx.send(embed=embed)
            return

        embed: discord.Embed = discord.Embed(
            title=profile.persona_name,
            description="님의 최근 게임 목록",
            url=user.get_profile_uri()
        )
        embed.set_thumbnail(url=profile.thumbnail_url)
        await ctx.send(embed=embed)

        games: list[SteamGame] = user.get_recent_games()
        if games == None:
            embed = getErrorEmbed("최근 게임 목록을 불러올 수 없습니다.")
            await ctx.send(embed=embed)
            return

        for game in games:
            embed: discord.Embed = discord.Embed(
                title=game["name"],
                url="https://store.steampowered.com/app/{0}".format(game.id),
            )
            embed.set_image(
                url="https://cdn.cloudflare.steamstatic.com/steam/apps/%s/header.jpg" % (game.id))
            embed.add_field(
                name="전체 플레이타임",
                value="%s시간%s분" % (game.playtime.h, game.playtime.m),
                inline=True,
            )
            embed.add_field(
                name="2주 플레이타임",
                value="%s시간%s분" % (game.playtime_2weeks.h,
                                   game.playtime_2weeks.m),
                inline=True,
            )
            await ctx.send(embed=embed)

    finally:

        await ldmsg.delete()


@bot.command()
async def ping(ctx: Context) -> None:
    if ctx.author.bot:
        return
    await ctx.send(f"{round(bot.latency * 1000)}ms")


@bot.command()
async def profile(ctx: Context):
    if ctx.author.bot:
        return
    
    ldmsg = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    try:

        url: URI = URI(ctx.message.content.split()[1])
        user: SteamUser = SteamUser.query_user(
            url) if url.is_valid() else SteamUser(url.to_string())
        if user == None:
            embed = getErrorEmbed("해당 유저를 찾을 수 없습니다.")
            await ctx.send(embed=embed)
            return

        profile: SteamProfile = user.get_profile()
        if profile == None:
            embed = getErrorEmbed("프로필을 불러오지 못했습니다.")
            await ctx.send(embed=embed)
            return
        
        embed: discord.Embed = discord.Embed(
            title=profile.persona_name,
            url="https://steamcommunity.com/profiles/%s"%(user.id)
        )

        embed.add_field(name="ID", value=user.id, inline=False)

        country: str = profile.contry_code
        if country != None:
            embed.add_field(name="Country", value=country, inline=False)

        level = user.get_level()
        if level != None:
            embed.add_field(name="Level", value=level, inline=False)

        created_time = profile.created_time
        if created_time != None:
            embed.add_field(name="Account Create Time",
                            value=created_time.strftime("%Y %m %d"), 
                            inline=False)

        game_count = user.get_owned_game_count()
        if game_count != None:
            embed.add_field(name="Game Count", value=game_count, inline=False)

        embed.set_thumbnail(url=profile.thumbnail_url)

        embed.set_footer(text="스팀 프로필 공개 범위 설정에 따라 결과가 달라질 수 있습니다.")

        await ctx.send(embed=embed)
        
    finally:
        
        await ldmsg.delete()


bot.run(TOKEN)
