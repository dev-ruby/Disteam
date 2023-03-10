import discord
import utils
from constants import TOKEN, EMOJIS

intents = discord.Intents.all()

client = discord.Client(intents=intents)


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.content.startswith("$"):
        return
    
    messages = message.content[1:].split()
    command = messages[0].lower()

    if command == "recentgame":
        loading_message = await message.channel.send(f"{EMOJIS.LOADING_EMOJI} Loading...")
        profile = utils.getUserInfo(messages[1])

        embed = discord.Embed(
            title=profile["personaname"],
            description="님의 최근 게임 목록",
            url="https://steamcommunity.com/profiles/{0}".format(messages[1]),
        )
        embed = embed.set_thumbnail(url=profile["avatarfull"])

        await message.channel.send(embed=embed)

        games = utils.getRecentGames(messages[1])

        for game in games:
            embed = discord.Embed(
                title=game["name"],
                url="https://store.steampowered.com/app/{0}".format(game["appid"]),
            )
            embed = embed.set_image(
                url="https://cdn.cloudflare.steamstatic.com/steam/apps/{0}/header.jpg".format(
                    game["appid"]
                )
            )
            embed = embed.add_field(
                name="전체 플레이타임",
                value="{0}시간{1}분".format(*divmod(game["playtime_forever"], 60)),
                inline=True,
            )
            embed = embed.add_field(
                name="2주 플레이타임",
                value="{0}시간{1}분".format(*divmod(game["playtime_2weeks"], 60)),
                inline=True,
            )

            await message.channel.send(embed=embed)

        await loading_message.delete()




client.run(TOKEN)
