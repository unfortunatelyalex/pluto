import os
import pytz
import json
import psutil
import random
import asyncio
import aiohttp
import requests
import datetime
import nextcord
from utils import *
from nextcord.utils import get
from dotenv import load_dotenv
from nextcord.ext import commands, application_checks
from nextcord.ui import Button, View
from nextcord.abc import GuildChannel
from nextcord.ext.commands import MissingRequiredArgument
from nextcord import Intents, Interaction, SlashOption, ChannelType, ButtonStyle


load_dotenv()

# Prefix load from .json file


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


helpGuide = json.load(open("help.json"))
intents = nextcord.Intents.default()
intents.message_content = True
embed_footer = 'made with 💛 by alex.#0017'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."
perminv = os.getenv("botinv")
dm_logs = "984869415684284536"


# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id="399668151475765258",
                   case_insensitive=True, intents=intents)
bot.remove_command('help')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# If you want to use spotify search
bot.spotify_credentials = {
    'client_id': os.getenv("Spotify_Client_ID"),
    'client_secret': os.getenv("Spotify_Client_Secret"),
}


# Ready up message and activity status
@bot.event
async def on_ready():
    print('--------------------------------')
    print(f"     Logged in as {bot.user} ")
    print(f" User-ID = {bot.user.id}")
    print(f"      Version = {nextcord.__version__}")
    print('--------------------------------')
    # Displays 'Competing in a massive gangbang'
    await bot.change_presence(activity=nextcord.CustomActivity(name="Nothing lasts forever but I wish we did", emoji="<:sadge:985124366561980476>"))
    # playing      = type 0, name="NAME"
    # streaming    = type 1, name="NAME", url=YOUTUBE/TWITCH
    # listening to = type 2, name="NAME"
    # watching     = type 3, name="NAME"
    # CUSTOM       = type 4 (NOT SUPPORTED)
    # COMPETING IN = type 5, name="NAME"
    logs = bot.get_channel(791670764143247420)
    onstart = nextcord.Embed(
        title=f"{bot.user.name} is now online",
        description="<@399668151475765258> read this <:point:916333529623846922>",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    onstart.set_author(
        name=bot.user,
        icon_url=f"{embed_footer_icon}"
    )
    onstart.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await logs.send(embed=onstart)
    if not os.path.exists("tempchannel.json"):
        with open("tempchannel.json", "w") as f:
            f.write("{}")
    with open("tempchannel.json", "r") as f:
        return json.load(f)


# Prefix create when bot joins server
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Prefix remove when bot leaves server


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop[str(guild.id)]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Deleted message log
@bot.event
async def on_message_delete(message):
    if message.guild.id == 791670762859266078:
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(
            title='Message Deleted', description=f'{message.author.mention} deleted the message: {message.content}\n In the channel {message.channel.mention}', color=0x00ff00)
        embed.set_footer(text=f'{message.author}',
                         icon_url=message.author.display_avatar)
        await channel.send(embed=embed)

# Edited message log


@bot.event
async def on_message_edit(before, after):
    if before.guild.id == 791670762859266078:
        if before.author.bot:
            return
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(
            title='Message Edited', description=f'{before.author.mention} edited the message: ```{before.content}``` to\n ```{after.content}```', color=0x00ff00)
        embed.set_footer(text=f'{before.author}',
                         icon_url=before.author.display_avatar)
        await channel.send(embed=embed)


# Dms from user to a channel
@bot.event
async def on_message(message: nextcord.Message):
    channel = bot.get_channel(984869415684284536)
    attachment = nextcord.Attachment
    if message.guild is None and not message.author.bot and isinstance(message.attachments, list):
        for attachment in message.attachments:
            if attachment.filename.endswith((".png", ".jpg", ".gif", ".jpeg", ".mp4", ".webm", ".mp3", ".wav", ".mov")):
                await channel.send(f"<@!399668151475765258>\n{message.author.mention} sent a picture: {attachment.url}\nMessage content: `{message.content}`")
                return
    if message.guild is None and not message.author.bot:
        await channel.send(f"<@!399668151475765258>\nNew message from {message.author.mention}:\nMessage content: `{message.content}`")
        await bot.process_commands(message)
        return
    if message.guild is not None:
        await bot.process_commands(message)
        return


# Dms a user
@bot.command(description="Let pluto DM someone if the user is in the same server as pluto", help=".dm <user> <message>")
async def dm(ctx, member: nextcord.Member, *, message):
    if ctx.author.guild_permissions.administrator == False:
        if ctx.author.id == 399668151475765258:
            embed = nextcord.Embed(
                title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
            embed.set_footer(text="This message was sent anonymously",
            icon_url=f"{embed_footer_icon}")
            await ctx.message.delete()
            await member.send(embed=embed)
            return
        await ctx.send(f"{missing_perms}")
        return
        
    if ctx.author.id != 399668151475765258:
        embed = nextcord.Embed(
            title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(
            text=f"This message was sent by {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.message.delete()
        await member.send(embed=embed)
        return

    else:
        embed = nextcord.Embed(
            title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(text="This message was sent anonymously",
                         icon_url=f"{embed_footer_icon}")
        await ctx.message.delete()
        await member.send(embed=embed)
        return


@bot.slash_command(description="Let pluto DM someone if the user is in the same server as pluto")
async def dm(interaction: Interaction, member: nextcord.Member = SlashOption(description="User to DM"), message=SlashOption(description="Message to be sent to the specified user")):
    if interaction.user.guild_permissions.administrator == False:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    if interaction.user.id != 399668151475765258:
        embed = nextcord.Embed(
            title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(text=f"This message was sent by {interaction.user}",
                         icon_url=interaction.user.display_avatar)
        await member.send(embed=embed)
        await interaction.response.send_message("Message was sent successfully", ephemeral=True)
        return

    else:
        embed = nextcord.Embed(
            title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(text="This message was sent anonymously",
                         icon_url=f"{bot.user.avatar.url}")
        await member.send(embed=embed)
        await interaction.response.send_message("Message was sent successfully", ephemeral=True)
        return


# Changeprefix command
@bot.command(aliases=['setprefix'], description="Changes the prefix. If empty, resets the prefix to default.", help=".prefix <new prefix>")
async def prefix(ctx, prefixset=None):
    if (not ctx.author.guild_permissions.administrator):
        await ctx.send(f'{missing_perms}')
        return
    if prefixset is None:
        prefixset = '.'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

        await ctx.send(f'The bots prefix has been changed to ``{prefixset}``')
        await ctx.message.add_reaction("✅")


@bot.command(description='Make the bot say something in a specific channel', help=".say <channel> <message>")
async def say(ctx, channel: nextcord.TextChannel, *, message):
    if ctx.author.guild_permissions.administrator == False:
        await ctx.send(f"{missing_perms}")
        return
    await channel.send(f"{message}", delete_after=3)


@bot.slash_command(description="Make the bot say something in a specific channel")
async def say(interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.text], description="Channel where the message should be sent to"), message=SlashOption(description="Message to be sent")):
    if interaction.user.guild_permissions.administrator == False:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    else:
        await channel.send(message)
        await interaction.response.send_message("Message was sent successfully", ephemeral=True)
        return


# CLEAR MESSAGES COMMAND
@bot.command(aliases=['claer', 'c'], description="Clears messages", help=".clear <amount>")
async def clear(ctx, amount: int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete. Usage: `.clear [NUMBER]`')


@bot.slash_command(description="Clears messages from the channel")
async def clear(interaction: Interaction, amount: int = SlashOption(description="Amount of messages to be deleted")):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(f"{missing_perms}", ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{amount} messages were successfully deleted", ephemeral=True)
    return


@bot.command(description="Purges the whole channel", help=".purge")
async def purge(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.response.send_message(f"{missing_perms}")
        return
    await ctx.channel.purge()


@bot.slash_command(description="Purges the whole channel")
async def purge(interaction: Interaction):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(f"{missing_perms}", ephemeral=True)
        return
    await interaction.channel.purge()
    await interaction.response.send_message("The channel was purged", ephemeral=True)
    return


# AVATAR COMMAND
@bot.command(aliases=["a", "av", "avtar", "avatr"], description="Displays a users avatar", help=".avatar <user>")
async def avatar(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar.url

    avatarEmbed = nextcord.Embed(
        title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatarEmbed.set_image(url=memberAvatar)
    avatarEmbed.set_footer(
        text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")

    await ctx.send(embed=avatarEmbed)


@bot.slash_command(description="Displays a users avatar")
async def avatar(interaction: Interaction, member: nextcord.Member = SlashOption(description="User to display the avatar of", required=False)):
    if member is None:
        member = interaction.user
    member_avatar = member.avatar.url

    avatar_embed = nextcord.Embed(
        title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatar_embed.set_image(url=member_avatar)
    avatar_embed.set_footer(
        text=f"{embed_footer}", icon_url=f"{bot.user.avatar.url}")

    await interaction.response.send_message(embed=avatar_embed)
    return


@bot.command(description="Posts a random dog picture from the dog api", help=".dog")
async def dog(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                await ctx.send(data['message'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.slash_command(description="Posts a random dog picture from the dog api")
async def dog(interaction: Interaction):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                await interaction.response.send_message(data['message'])
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(description="Posts a random cat picture from the cat api", help=".cat")
async def cat(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                data = await r.json()
                await ctx.send(data['file'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.slash_command(description="Posts a random cat picture from the cat api")
async def cat(interaction: Interaction):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                data = await r.json()
                await interaction.response.send_message(data['file'])
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(aliases=["inv"], description="Sends the bots invite link", help=".invite")
async def invite(ctx):
    await ctx.send("pluto isn't public, stfu")


@bot.slash_command(description="Sends the bot invite link")
async def invite(interaction: Interaction):
    await interaction.response.send_message("pluto isn't public, stfu")


@bot.command(description="Posts a random meme from the dankmemes subreddit", help=".meme")
async def meme(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.slash_command(description="Posts a random meme from the dankmemes subreddit")
async def meme(interaction: Interaction):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/memes/random.json') as r:
                data = await r.json()
                await interaction.response.send_message(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(aliases=["uinfo", "ui", "uinf"], description="Information about the user", help=".userinfo <user>")
async def userinfo(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.author
    fetch_user = await ctx.bot.fetch_user(user.id)
    embed = nextcord.Embed(title=f'Userinfo for {user.name}', color=0x202225)
    if user.avatar is not None:
        embed.set_thumbnail(
            url=f"{user.avatar.url}"
        )
    else:
        embed.set_thumbnail(
            url=f"{user.default_avatar.url}"
        )
    if ctx.author.avatar is not None:
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.avatar.url}"
        )
    else:
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.default_avatar.url}"
        )
    embed.add_field(
        name="General Info",
        value=f"> Joined Discord on `{user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> Joined Server on: `{user.joined_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{user.id}` \n> Is bot?: `{user.bot}`",
        inline=False
    )
    if fetch_user.banner is not None:
        embed.add_field(
            name="Profile",
            value=f"> Banner: [View]({fetch_user.banner.url}) \n> Avatar: [View]({user.avatar.url})",
            inline=False
        )
    else:
        embed.add_field(
            name="Profile",
            value=f"> Banner: `NONE` \n> Avatar: [View]({user.avatar.url})",
            inline=False
        )
    roles = " ".join(
        [role.mention for role in user.roles if role.name != "@everyone"])
    embed.add_field(
        name="Server Info",
        value=f"> Nickname: `{user.nick}` \n> Roles (**{len(user.roles)}**): {roles} @everyone",
        inline=False
    )
    # roles = " ".join([role.mention for role in user.roles if role.name != "@everyone"])
    # if roles == "":
    #     embed.add_field(
    #         name="Roles",
    #         value="None",
    #         inline=True
    #     )
    # else:
    #     embed.add_field(
    #         name="Roles",
    #         value=f"{roles}",
    #         inline=True
    #     )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.avatar.url
    )
    await ctx.send(embed=embed)


@bot.slash_command(description="Information about a user")
async def userinfo(interaction: Interaction, user: nextcord.Member = SlashOption(description='User to get info about', required=False)):
    if user is None:
        user = interaction.user
    fetch_user = await bot.fetch_user(user.id)
    embed = nextcord.Embed(title=f'Userinfo for {user.name}', color=0x202225)
    if user.avatar is not None:
        embed.set_thumbnail(
            url=f"{user.avatar.url}"
        )
    else:
        embed.set_thumbnail(
            url=f"{user.default_avatar.url}"
        )
    if interaction.user.avatar is not None:
        embed.set_author(
            name=f"{interaction.user.name}#{interaction.user.discriminator}",
            icon_url=f"{interaction.user.avatar.url}"
        )
    else:
        embed.set_author(
            name=f"{interaction.user.name}#{interaction.user.discriminator}",
            icon_url=f"{interaction.user.default_avatar.url}"
        )
    embed.add_field(
        name="General Info",
        value=f"> Joined Discord on `{user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> Joined Server on: `{user.joined_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{user.id}` \n> Is bot?: `{user.bot}`",
        inline=False
    )
    if fetch_user.banner is not None:
        embed.add_field(
            name="Profile",
            value=f"> Banner: [View]({fetch_user.banner.url}) \n> Avatar: [View]({user.avatar.url})",
            inline=False
        )
    else:
        embed.add_field(
            name="Profile",
            value=f"> Banner: `NONE` \n> Avatar: [View]({user.avatar.url})",
            inline=False
        )
    roles = " ".join(
        [role.mention for role in user.roles if role.name != "@everyone"])
    embed.add_field(
        name="Server Info",
        value=f"> Nickname: `{user.nick}` \n> Roles (**{len(user.roles)}**): {roles} @everyone",
        inline=False
    )
    # roles = " ".join([role.mention for role in user.roles if role.name != "@everyone"])
    # if roles == "":
    #     embed.add_field(
    #         name="Roles",
    #         value="None",
    #         inline=True
    #     )
    # else:
    #     embed.add_field(
    #         name="Roles",
    #         value=f"{roles}",
    #         inline=True
    #     )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.avatar.url
    )
    await interaction.send(embed=embed)





@bot.command(aliases=["ab", "abme", "aboutme"], description="Information about the bot", help=".about")
async def about(ctx):
    embed = nextcord.Embed(title=f'About {bot.user.name}', color=0x202225)
    embed.set_thumbnail(
        url=f"{bot.user.avatar.url}"
    )
    embed.add_field(
        name="General Info",
        value=f"> Created on `{bot.user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{bot.user.id}`",
        inline=False
    )
    embed.add_field(
        name="Profile",
        value=f"> Avatar: [View]({bot.user.avatar.url})",
        inline=False
    )
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    embed.add_field(
        name="Host",
        value=f"> CPU usage: {psutil.cpu_percent(interval=1)}% \n> RAM usage: {round(mem)}MB",
        inline=False
    )
    embed.add_field(
        name="About Me",
        value=f"> Guild count: `{len(bot.guilds)}` \n> Line count: `{len(open('main.py').readlines())}` \n> Made by: `@alex.#0017`",
        inline=False
    )
    if ctx.author.avatar is not None:
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.avatar.url}"
        )
    else:
        embed.set_author(
            name=f"{ctx.author.name}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.default_avatar.url}"
        )
    await ctx.send(embed=embed)


@bot.slash_command(description="Information about the bot")
async def about(interaction: Interaction):
    embed = nextcord.Embed(title=f'About {bot.user.name}', color=0x202225)
    embed.set_thumbnail(
        url=f"{bot.user.avatar.url}"
    )
    embed.add_field(
        name="General Info",
        value=f"> Created on `{bot.user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{bot.user.id}`",
        inline=False
    )
    embed.add_field(
        name="Profile",
        value=f"> Avatar: [View]({bot.user.avatar.url})",
        inline=False
    )
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    embed.add_field(
        name="Host",
        value=f"> CPU usage: {psutil.cpu_percent(interval=1)}% \n> RAM usage: {round(mem)}MB",
        inline=False
    )
    embed.add_field(
        name="About Me",
        value=f"> Guild count: `{len(bot.guilds)}` \n> Line count: `{len(open('main.py').readlines())}` \n> Made by: `@alex.#0017`",
        inline=False
    )
    if interaction.user.avatar is not None:
        embed.set_author(
            name=f"{interaction.user.name}#{interaction.user.discriminator}",
            icon_url=f"{interaction.user.avatar.url}"
        )
    else:
        embed.set_author(
            name=f"{interaction.user.name}#{interaction.user.discriminator}",
            icon_url=f"{interaction.user.default_avatar.url}"
        )
    await interaction.send(embed=embed)





@bot.command(description="Yo Mama!", help=".roastme")
async def roastme(ctx):
    try:
        with open('roastme.json', encoding="utf8") as f:
            data = json.load(f)
        category = random.choice(list(data.keys()))
        roast = random.choice(data[category])
        await ctx.send(f'{roast}')
    except Exception as e:
        await ctx.send(f'{e}')


@bot.slash_command(description="Yo Mama!")
async def roastme(interaction: Interaction):
    try:
        with open('roastme.json', encoding="utf8") as f:
            data = json.load(f)
        category = random.choice(list(data.keys()))
        roast = random.choice(data[category])
        await interaction.response.send_message(f'{roast}')
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(description="Posts a random image from the nsfw subreddit", help=".nsfw")
async def nsfw(ctx):
    if ctx.channel.is_nsfw() is False:
        await ctx.send(f'You can\'t run this command in a non-nsfw channel')
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/nsfw/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.slash_command(description="Posts a random image or video from the nsfw subreddit")
async def nsfw(interaction: Interaction):
    if interaction.channel.is_nsfw() is False:
        await interaction.response.send_message(f'You can\'t run this command in a non-nsfw channel')

        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/nsfw/random.json') as r:
                data = await r.json()
                await interaction.response.send_message(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(description="Well....it's an hentai api", help=".hentai <endpoint>")
async def hentai(ctx, *, search):
    if ctx.channel.is_nsfw() is False:
        await ctx.send(f'You can\'t run this command in a non-nsfw channel')
        return
    if search == "list":
        list = nextcord.Embed(
            title="NSFW Tags",
            description="List of all the nsfw tags"
        )
        list.add_field(
            name="Anal",
            value="Basically cock in ass or something"
        )
        list.add_field(
            name="Blowjob",
            value="You know blowjob. Giving head and stuff"
        )
        list.add_field(
            name="Cum",
            value="Ejaculation"
        )
        list.add_field(
            name="Fuck",
            value="Classic fuck"
        )
        list.add_field(
            name="Neko",
            value="Catgirls!!!!!!"
        )
        list.add_field(
            name="Pussylick",
            value="Pretty self explanatory"
        )
        list.add_field(
            name="Solo",
            value="Alone <:6524skulldark:948990530161872956>\nNo bitches? <:what:955183802974609438>"
        )
        list.add_field(
            name="Yaoi",
            value="Anime....but gay"
        )
        list.add_field(
            name="Yuri",
            value="Anime....but lesbian"
        )
        await ctx.send(embed=list)
    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://purrbot.site/api/img/nsfw/{search}/gif') as r:
                    data = await r.json()
                    await ctx.send(data['link'])
        except Exception as e:
            await ctx.send(f'{e}')


@hentai.error
async def hentai_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Please provide an endpoint. Use `.hentai list` to see all the tags")


@bot.slash_command(description="It's hentai, you know what hentai is.")
async def hentai(interaction: Interaction, category: str = SlashOption(name="category", description="The hentai category", choices={"anal": "anal", "blowjob": "blowjob", "cum": "cum", "fuck": "fuck", "neko": "neko", "pussylick": "pussylick", "solo": "solo", "yaoi": "yaoi", "yuri": "yuri"})):
    if interaction.channel.is_nsfw() is False:
        await interaction.send(f'You can\'t run this command in a non-nsfw channel')
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://purrbot.site/api/img/nsfw/{category}/gif') as r:
                data = await r.json()
                await interaction.response.send_message(data['link'])
    except Exception as e:
        await interaction.response.send_message(f'{e}')


@bot.command(description="Let pluto remind you of something", help=".remind <time> <reminder>")
async def remind(ctx, time, *, reminder):
    print(time)
    print(reminder)
    embed = nextcord.Embed(
        color=0x55a7f7, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    seconds = 0
    if reminder is None:
        # Error message
        embed.add_field(
            name='Warning', value='Please specify what do you want me to remind you about.')
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 5:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(
            name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hello {ctx.author.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    await ctx.send(embed=embed)


@bot.slash_command(description="Let pluto remind you of something")
async def remind(interaction: Interaction, time: str = SlashOption(description='Example: Seconds = "5s" / Minutes = "5m" / Hours = "5h" / Days = "5d"'), reminder: str = SlashOption(description='The reminder message')):
    seconds = 0
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
        await interaction.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        print(
            f"User {interaction.user.name} has requested the reminder  --  {reminder}  --  for {counter}")
        await asyncio.sleep(seconds)
        await interaction.send(f"Hello {interaction.user.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
        await interaction.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        print(
            f"User {interaction.user.name} has requested the reminder  --  {reminder}  --  for {counter}")
        await asyncio.sleep(seconds)
        await interaction.send(f"Hello {interaction.user.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
        await interaction.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        print(
            f"User {interaction.user.name} has requested the reminder  --  {reminder}  --  for {counter}")
        await asyncio.sleep(seconds)
        await interaction.send(f"Hello {interaction.user.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
        await interaction.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        print(
            f"User {interaction.user.name} has requested the reminder  --  {reminder}  --  for {counter}")
        await asyncio.sleep(seconds)
        await interaction.send(f"Hello {interaction.user.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    else:
        await interaction.send(f"Unexpected error. I dont even know what went wrong. <@!399668151475765258> pls fix this")


# MODERATION
@bot.command(description="Kicks a user", help=".kick <user> <reason>")
async def kick(ctx, member: nextcord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.reply("You can't kick yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.reply(f'{missing_perms}')
        return
    if reason is None:
        await ctx.reply("You need to specify a reason to kick this user")
        return
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked.")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to kick.")
            return


@bot.slash_command(description="Kicks a user")
async def kick(interaction: Interaction, member: nextcord.Member = SlashOption(description="The member to kick"), reason: str = SlashOption(description="The reason for the kick", required=False)):
    if member == interaction.user:
        await interaction.response.send_message("You can't kick yourself, idiot. *Who hired this guy?*")
        return
    # if the interaction user doesn't have permissions to kick members, send a message and return
    if (not interaction.user.guild_permissions.kick_members):
        await interaction.response.send_message(f'{missing_perms}')
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been kicked.")


@bot.command(description="Bans a user", help=".ban <user> <reason>")
async def ban(ctx, member: nextcord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.reply("You can't ban yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.reply(f'{missing_perms}')
        return
    if reason is None:
        await ctx.reply("You need to specify a reason to ban this user")
        return

    await ctx.send(f"{member} has been banned.")
    await member.send(f"You have been banned in `{ctx.guild}`\nReason: `{reason}`")
    async with member.typing():
        await asyncio.sleep(3)
    await member.ban(reason=reason)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to ban.")
            return


@bot.slash_command(description="Bans a user")
async def ban(interaction: Interaction, member: nextcord.Member = SlashOption(description="The member to ban"), reason: str = SlashOption(description="The reason for the ban", required=False)):
    if member == interaction.user:
        await interaction.response.send_message("You can't ban yourself, idiot. *Who hired this guy?*")
        return
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(f'{missing_perms}', ephemeral=True)
        return
    await interaction.response.send_message(f"{member} has been banned.")
    await member.ban(reason=reason)


@bot.command(description="Blind the user, making him unable to see other channels", help=".blind <user>")
async def blind(ctx, member: nextcord.Member):
    if ctx.guild.id != 791670762859266078:
        await ctx.send("This command is only available in a specific server.")
        return
    if member == ctx.author:
        await ctx.reply("You can't blind yourself, idiot. *Who hired this guy?*")
        return
    role = ctx.guild.get_role(984816627746996305)
    await member.edit(roles=[role])


@blind.error
async def blind_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to blind.")
            return


@bot.slash_command(description="Blind the user, making him unable to see other channels")
async def blind(interaction: Interaction, member: nextcord.Member = SlashOption(description="The member to blind")):
    if interaction.guild.id != 791670762859266078:
        await interaction.send("This command is only available in a specific server.", ephemeral=True)
        return
    if member == interaction.user:
        await interaction.response.send_message("You can't blind yourself, idiot. *Who hired this guy?*")
        return
    blind_role = interaction.guild.get_role(984816627746996305)
    await member.edit(roles=[])
    await member.add_roles(blind_role)
    await interaction.response.send_message(f"{member.mention} has been successfully blinded.")


@bot.command(description="Scan a file with Virustotal", help=".scan <file>")
async def scan(ctx, *args):
    if ctx.message.attachments:
        isfile = True

        await ctx.send('Downloading file...')
        file = ctx.message.attachments[0]
        await file.save(file.filename)

        await ctx.send('Sending to VT...')
        localfile = open(file.filename, 'rb')
        scanid = requests.post(
            'https://www.virustotal.com/api/v3/files',
            headers={'x-apikey': os.getenv("Virustotal")},
            files={'file': (file.filename, localfile)}
        ).json()['data']['id']
        localfile.close()

        await ctx.send('Deleting file from server...')
        os.remove(file.filename)
    else:
        isfile = False
        await ctx.send('Sending to VT...')

        scanid = requests.post(
            'https://www.virustotal.com/api/v3/urls',
            headers={'x-apikey': os.getenv("Virustotal")},
            data={f'url': str(args[0])}
        ).json()['data']['id']

    await ctx.send('Scanning...(this can take a while)')
    scanresult = requests.get(
        f'https://www.virustotal.com/api/v3/analyses/{scanid}',
        headers={'x-apikey': os.getenv("Virustotal")}
    ).json()['data']['attributes']

    while scanresult['status'] != 'completed':
        scanresult = requests.get(
            f'https://www.virustotal.com/api/v3/analyses/{scanid}',
            headers={'x-apikey': os.getenv("Virustotal")}
        ).json()['data']['attributes']
        await asyncio.sleep(0.1)

    await ctx.send('Fetching scan results...')
    stats = scanresult['stats']
    engines = int(stats['malicious']) + \
        int(stats['undetected']) + int(stats['harmless'])
    scans = scanresult['results']

    ismalw = ':warning: marked as malicious'
    color = 0xf58f14

    trusted_engines_detect = False
    try:
        trusted_engines_detect = (
            (scans['Dr.Web']['result'] != 'clean' and scans['Dr.Web']['result'] != None) or
            (scans['DrWeb']['result'] != 'clean' and scans['DrWeb']['result'] != None) or
            (scans['BitDefender']['result'] !=
             'clean' and scans['BitDefender']['result'] != None)
        )
    except KeyError:
        pass

    if (stats['malicious'] > 3) or trusted_engines_detect:
        ismalw = 'malware!!!!!'
        color = 0xd13434
    else:
        ismalw = 'clean'
        color = 0x36b338

    resultstr = ''
    i = 0

    show_engines = []
    if (len(args) > 1) and (not isfile):
        show_engines = str(args[1]).split(',')
    elif (len(args) > 0) and (isfile):
        show_engines = str(args[0]).split(',')

    for engine in scans:
        if (not show_engines) and (i < 10):
            resultstr += f'**{engine}** - `{scans[engine]["result"]}`\n'
            i += 1
        elif (show_engines):
            for reqengine in show_engines:
                if reqengine == engine:
                    resultstr += f'**{engine}** - `{scans[engine]["result"]}`\n'
        else:
            break

    scantype = 'file' if isfile else 'URL'
    resultmsg = nextcord.Embed(
        color=color, title=f'The {scantype} is {ismalw} ({stats["malicious"]}/{engines})', description=resultstr)
    await ctx.reply(embed=resultmsg)


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        if after.channel.name == "voice chat erstellen":
            # create a new file called "tempchannel.json"
            # format it to a dictionary
            # per dictonary, create a new channel
            with open("tempchannel.json", "r") as f:
                data = json.load(f)
            channel = await create_voice_channel(after.channel.guild, f"{member.name}".lower(), category_name="idek")
            move_lobby = await create_voice_channel(after.channel.guild, f"⬆ {member.name} Lobby".lower(), category_name="idek")
            # write the channel and movelobby to the file
            data[f"{member.name}".lower()] = channel.id
            data[f"{member.name}".lower() + "lobby"] = move_lobby.id
            with open("tempchannel.json", "w") as f:
                json.dump(data, f, indent=4)

            await channel.set_permissions(member, connect=True, speak=True, move_members=True)
            await move_lobby.set_permissions(member, connect=True, speak=True, move_members=True)
            await channel.set_permissions(after.channel.guild.default_role, view_channel=False, connect=False)
            await channel.set_permissions(after.channel.guild.get_role(985205310740389918), view_channel=True, connect=False)
            await move_lobby.set_permissions(after.channel.guild.default_role, view_channel=False, connect=False)
            await move_lobby.set_permissions(after.channel.guild.get_role(985205310740389918), view_channel=True, connect=True)

            if channel is not None:
                await member.move_to(channel)

    if before.channel is not None:
        if before.channel.category.id == get_category_by_name(before.channel.guild, "idek").id:
            # set move_lobby as a variable to avoid errors
            move_lobby = get_channel_by_name(
                before.channel.guild, f"⬆ {member.name} Lobby".lower())

            # check if a voice channel in tempchannel.json is empty, if so, delete it
            with open("tempchannel.json", "r") as f:
                data = json.load(f)
            if data[f"{member.name}".lower()] is not None:
                channel = get(before.channel.guild.channels,
                              id=data[f"{member.name}".lower()])
                if channel is not None:
                    if len(channel.members) == 0:
                        await channel.delete()
                        await move_lobby.delete()
                        # delete both channels from the file
                        data[f"{member.name}".lower()] = None
                        data[f"{member.name}".lower() + "lobby"] = None
                        with open("tempchannel.json", "w") as f:
                            json.dump(data, f, indent=4)


def createHelpEmbed(pageNum=0, inline=True):
    pageNum = (pageNum) % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed = nextcord.Embed(color=0x0080ff, title=pageTitle,
                           timestamp=datetime.datetime.now(datetime.timezone.utc))
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name="/"+key, value=val, inline=True)
        embed.set_footer(
            text=f"{embed_footer} | Page {pageNum+1} of {len(list(helpGuide))}", icon_url=f"{bot.user.display_avatar}")
    return embed


@bot.command(name="help", description="Shows every command and its description")
async def help(ctx):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    previousButton = Button(label="<", style=ButtonStyle.blurple)
    nextButton = Button(label=">", style=ButtonStyle.blurple)
    previousButton.callback = previous_callback
    nextButton.callback = next_callback

    myview = View(timeout=180)
    myview.add_item(previousButton)
    myview.add_item(nextButton)

    sent_msg = await ctx.send(embed=createHelpEmbed(currentPage), view=myview)


@bot.slash_command(name="help", description="Shows every command and its description")
async def help(interaction: Interaction):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    previousButton = Button(label="<", style=ButtonStyle.blurple)
    nextButton = Button(label=">", style=ButtonStyle.blurple)
    previousButton.callback = previous_callback
    nextButton.callback = next_callback

    myview = View(timeout=180)
    myview.add_item(previousButton)
    myview.add_item(nextButton)

    sent_msg = await interaction.send(embed=createHelpEmbed(currentPage), view=myview)


@bot.slash_command(description="Restarts the bot.")
async def restart(interaction: Interaction):
    restartembed = nextcord.Embed(
        title=f"{bot.user.name} is now restarting...",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    restartembed.set_author(
        name=interaction.user.name,
        icon_url=interaction.user.avatar.url,
    )
    restartembed.set_footer(
        text=f"{embed_footer}",
        icon_url=f"{bot.user.avatar.url}"
    )
    if interaction.user.id != 399668151475765258:
        await interaction.send(f'{not_owner}')
        return

    await interaction.send(embed=restartembed, ephemeral=True)

    await bot.close()


# Elias ersatz

@bot.command(description="Self roles")
async def rr(ctx):

    # if author doesn't have admin permissions, return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permissions to send this command", delete_after=3)
        return

    young = Button(label="13-15", style=ButtonStyle.blurple)
    young_role = nextcord.utils.get(ctx.guild.roles, name="13-15")

    middle = Button(label="15-17", style=ButtonStyle.blurple)
    middle_role = nextcord.utils.get(ctx.guild.roles, name="15-17")

    old = Button(label="18+", style=ButtonStyle.blurple)
    old_role = nextcord.utils.get(ctx.guild.roles, name="18+😳")

    man = Button(label="Männlich", style=ButtonStyle.blurple)
    man_role = nextcord.utils.get(ctx.guild.roles, name="Männlich")

    girl = Button(label="Weiblich", style=ButtonStyle.blurple)
    girl_role = nextcord.utils.get(ctx.guild.roles, name="Weiblich")

    divers = Button(label="Divers", style=ButtonStyle.red)
    divers_role = nextcord.utils.get(ctx.guild.roles, name="Divers")

    async def young_callback(interaction):
        if young_role in interaction.user.roles:
            await interaction.user.remove_roles(young_role)
            await interaction.send("Dir wurde die Rolle `13-15` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(young_role)
            await interaction.send("Dir wurde die Rolle `13-15` gegeben", ephemeral=True)
    young.callback = young_callback

    async def middle_callback(interaction):
        if middle_role in interaction.user.roles:
            await interaction.user.remove_roles(middle_role)
            await interaction.send("Dir wurde die Rolle `15-17` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(middle_role)
            await interaction.send("Dir wurde die Rolle `15-17` gegeben", ephemeral=True)
    middle.callback = middle_callback

    async def old_callback(interaction):
        if old_role in interaction.user.roles:
            await interaction.user.remove_roles(old_role)
            await interaction.send("Dir wurde die Rolle `18+` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(old_role)
            await interaction.send("Dir wurde die Rolle `18+` gegeben", ephemeral=True)
    old.callback = old_callback

    async def man_callback(interaction):
        if man_role in interaction.user.roles:
            await interaction.user.remove_roles(man_role)
            await interaction.send("Dir wurde die Rolle `Männlich` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(man_role)
            await interaction.send("Dir wurde die Rolle `Männlich` gegeben", ephemeral=True)
    man.callback = man_callback

    async def girl_callback(interaction):
        if girl_role in interaction.user.roles:
            await interaction.user.remove_roles(girl_role)
            await interaction.send("Dir wurde die Rolle `Weiblich` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(girl_role)
            await interaction.send("Dir wurde die Rolle `Weiblich` gegeben", ephemeral=True)
    girl.callback = girl_callback

    async def divers_callback(interaction):
        if divers_role in interaction.user.roles:
            await interaction.user.remove_roles(divers_role)
            await interaction.send("Dir wurde die Rolle `Divers` weggenommen", ephemeral=True)
        else:
            await interaction.user.add_roles(divers_role)
            await interaction.send("Dir wurde die Rolle `Divers` gegeben", ephemeral=True)
    divers.callback = divers_callback

    buttonsxd = View(timeout=99999999999)
    buttonsxd.add_item(young)
    buttonsxd.add_item(middle)
    buttonsxd.add_item(old)
    buttonsxd.add_item(man)
    buttonsxd.add_item(girl)
    buttonsxd.add_item(divers)

    embed = nextcord.Embed(title="Reaction Roles",
                           description="Click on the buttons to get your roles")
    embed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.message.delete()
    await ctx.send(embed=embed, view=buttonsxd)


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
