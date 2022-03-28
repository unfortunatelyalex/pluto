import asyncio
import os
import aiohttp
import random
import json
import datetime
import re
import requests
import subprocess
import urllib.parse
import urllib.request
import nextcord
import yt_dlp
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio
from nextcord.ext import commands
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands.core import has_permissions
from dotenv import load_dotenv


load_dotenv()

# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id="399668151475765258", case_insensitive=True)

intents = nextcord.Intents().all()
yt_dlp.utils.bug_reports_message = lambda: ''
connected_to_vc = False
intents.members = True
clown1 = '🤡'
clown2 = '<:literalclown:903780300839088188>'
clown3 = '<a:thumbsclown:931491107546738729>'
clown4 = '<:deadclown:931491107148300318>'
clown5 = '<:imdead:953579229293989958>'
clown6 = '<:6323trollskull:948990530359029821>'
clown7 = '<:6970realisticskull:948990530287722516>'
clown8 = '<:6682imdead:948990530241572915>'
clown9 = '<a:6434skellyfuckya:948990531298545695>'
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."
perminv = "https://discord.com/api/oauth2/authorize?client_id=791670415779954698&permissions=137707659350&scope=bot"
ytdl_format_options = {'format': 'bestaudio',
                       'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                       'restrictfilenames': True,
                       'no-playlist': True,
                       'nocheckcertificate': True,
                       'ignoreerrors': False,
                       'logtostderr': False,
                       'geo-bypass': True,
                       'quiet': True,
                       'no_warnings': True,
                       'default_search': 'auto',
                       'source_address': '0.0.0.0'}
ffmpeg_options = {'options': '-vn'}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
# play_queue with automatic id continuation

play_queue = []
player_obj_queue = []
servers = []  # TODO: add support for multiple servers
current_server = None
for file in os.listdir():
    if file.endswith('.webm'): os.remove(file)





# Ready up message and activity status
@bot.event
async def on_ready():
    print('--------------------------------')
    print(f"     Logged in as {bot.user} ")
    print(f" User-ID = {bot.user.id}")
    print(f"      Version = {nextcord.__version__}")
    print('--------------------------------')
    await bot.change_presence(activity=nextcord.Activity(type=2, name="your bullshit")) # Displays 'Competing in a massive gangbang'
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
        icon_url=f"{embed_footer_icon}",
    )
    onstart.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await logs.send(embed=onstart)





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






# Test command
@bot.command(aliases=['hi'], description='Test if the bot is able to chat', help="Says hello. What a nice bot.")
async def hello(ctx):
    await ctx.send('hello :)')





# Changeprefix command
@bot.command(aliases=['setprefix'], description="Usage: .prefix [NEW PREFIX]", help="Changes the prefix. If empty, resets the prefix to default.")
async def prefix(ctx, prefixset=None):
    if (not ctx.author.guild_permissions.administrator):
        await ctx.send(f'{missing_perms}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
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
    

        




# Token command
@bot.command(aliases=['key', 'api', 'apikey'], description='Usage: .token', help="Try me")
async def token(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.channel.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)

    if ctx.author.id == 399668151475765258:
        await ctx.channel.send('You got jebaited')










@bot.command(description='Usage: .mute [@USER]', help="TEMPORARILY DISABLED")
@has_permissions(manage_messages = True)
async def mute(ctx, member:nextcord.Member):
    if ctx.author.id != 399668151475765258:
        await ctx.channel.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    role = nextcord.utils.get(ctx.guild.roles, name='Mommy')
    await member.add_roles(role)

@bot.command(description='Usage: .unmute [@USER]', help="TEMPORARILY DISABLED")
@has_permissions(manage_messages = True)
async def unmute(ctx, member:nextcord.Member):
    if ctx.author.id != 399668151475765258:
        await ctx.channel.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    role = nextcord.utils.get(ctx.guild.roles, name='Mommy')
    await member.remove_roles(role)






@bot.command(description='Usage: .say [#CHANNEL] [MESSAGE]', help="Make the bot say something in a specific channel")
async def say(ctx, channel: nextcord.TextChannel, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.channel.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await channel.send(f"{message}")







@bot.command(aliases=['em'], description="Usage: .embed [YOUR TEXT]", help="Embedded test message")
async def embed(ctx, message = None, name = None, value = None):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    
    if message is None:
        message = "not defined"
    embed = nextcord.Embed(
        title=f"Test message includes: {message}",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    embed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar.url,
    )
    embed.set_footer(
        text=f"{embed_footer}",
        icon_url=f"{embed_footer_icon}"
    )
    embed.add_field(
        name=f"{name}",
        value=f"{value}"
    )
    await ctx.send(embed=embed)





# CLEAR MESSAGES COMMAND
@bot.command(aliases=['claer', 'c'], description="Usage: .clear [Amount of messages you want to delete]", help="Clears messages")
async def clear(ctx, amount : int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await ctx.channel.purge(limit=amount + 1)

@bot.command(aliases=['p'], description="Usage: .purge", help="Purges the whole channel")
async def purge(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await ctx.channel.purge()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete. Usage: .clear [NUMBER]')






# AVATAR COMMAND
@bot.command(aliases=["a", "av", "avtar", "avatr"], description="Usage: .avatar [USER @]", help="Displays a users avatar")
async def avatar(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar.url

    avatarEmbed = nextcord.Embed(title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatarEmbed.set_image(url=memberAvatar)
    avatarEmbed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")

    await ctx.send(embed=avatarEmbed)








# **ONLINE**
@bot.command(description="Usage: .online", help="Changes the online status to online")
async def online(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(status=nextcord.Status.online,activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟢')

# **IDLE**
@bot.command(description="Usage: .idle", help="Changes the online status to idle")
async def idle(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟡')

# **DO NOT DISTURB**
@bot.command(description="Usage: .dnd", help="Changes the online status to dnd")
async def dnd(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🔴')

# **INVISIBLE**
@bot.command(description="Usage: .invisible", help="Changes the online status to invisible")
async def invisible(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(status=nextcord.Status.invisible, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('⚪')





# PLAYING
@bot.command(description="Usage: .playing [GAME]", help="Changes the bots activity status to 'playing ...'")
async def playing(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(activity=nextcord.Activity(type=0, name=message))
    await ctx.message.add_reaction('👌')
@playing.error
async def playing_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what game I should play.')


# LISTENING TO
@bot.command(description="Usage: .listening [SONG]", help="Changes the bots activity status to 'listening to ...'")
async def listening(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(activity=nextcord.Activity(type=2, name=message))
    await ctx.message.add_reaction('👌')
@listening.error
async def listening_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what song I should listen to.')


# WATCHING
@bot.command(description="Usage: .watching [VIDEO]", help="Changes the bots activity status to 'watching ...'")
async def watching(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(activity=nextcord.Activity(type=3, name=message))
    await ctx.message.add_reaction('👌')
@watching.error
async def watching_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what video I should watch.')


# COMPETING IN
@bot.command(description="Usage: .competing [ACTIVITY]", help="Changes the bots activity status to 'competing in ...'")
async def compete(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
    await bot.change_presence(activity=nextcord.Activity(type=5, name=message))
    await ctx.message.add_reaction('👌')
@compete.error
async def compete_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify the activity I should compete in')










## create a ping command that responds with the bots latency
@bot.command(description="Usage: .ping", help="Returns the bots latency")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.message.add_reaction('👌')




# create an event that stores deleted messages in a specific channel 
@bot.event
async def on_message_delete(message):
    if message.guild.id == 791670762859266078:
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(title='Message Deleted', description=f'{message.author.mention} deleted the message: {message.content}\n In the channel {message.channel.mention}', color=0x00ff00)
        embed.set_footer(text=f'{message.author}', icon_url=message.author.display_avatar)
        await channel.send(embed=embed)
        await message.delete()


# create an event that stores edited messages in a specific channel
@bot.event
async def on_message_edit(before, after):
    if before.guild.id == 791670762859266078:
        if before.author.bot:
            return
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(title='Message Edited', description=f'{before.author.mention} edited the message: ```{before.content}``` to\n ```{after.content}```', color=0x00ff00)
        embed.set_footer(text=f'{before.author}', icon_url=before.author.display_avatar)
        await channel.send(embed=embed)


# create a dog command that posts dog pictures from the dog api
@bot.command(description="Usage: .dog", help="Posts a random dog picture from the dog api")
async def dog(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                await ctx.send(data['message'])
    except Exception as e:
        await ctx.send(f'{e}')


# create a cat command that posts cat pictures from the cat api
@bot.command(description="Usage: .cat", help="Posts a random cat picture from the cat api")
async def cat(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                data = await r.json()
                await ctx.send(data['file'])
    except Exception as e:
        await ctx.send(f'{e}')


# create an invite command that sends the perminv variable
@bot.command(aliases=["inv"], description="Usage: .invite", help="Sends the bots invite link")
async def invite(ctx):
    await ctx.send(f'{perminv}')


# create a meme command that posts random memes from the dankmemes and memes subreddit
@bot.command(description="Usage: .meme", help="Posts a random meme from the dankmemes and memes subreddit")
async def meme(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')
        


# create a help command that returns every command and its description
# @bot.command(description="Usage: .help", help="Returns every command and its description")
# async def help(ctx):
#     embed = nextcord.Embed(title='Help', description='Here are all of the commands for the bot', color=0x00ff00)
#     # add a field for the prefix command and its description
#     embed.add_field(name='Prefix', value='Changes the bots prefix', inline=False)
#     # add a field for the avatar command and its description
#     embed.add_field(name='Avatar', value='Let\'s you look at other\'s avatar\'s', inline=False)
#     # add a field for the clear command with its description
#     embed.add_field(name='Clear', value='Clears a certain amount of messages', inline=False)
#     embed.add_field(name='Ping', value='Returns the bots latency', inline=False)
#     embed.add_field(name='Invite', value='Sends the bots invite link', inline=False)
#     embed.add_field(name='Dog', value='Posts a random dog picture from the dog api', inline=False)
#     embed.add_field(name='Cat', value='Posts a random cat picture from the cat api', inline=False)
#     embed.add_field(name='Meme', value='Posts a random meme from the dankmemes and memes subreddit', inline=False)
#     embed.add_field(name='Help', value='Returns every command and its description', inline=False)
#     embed.add_field(name='Listening', value='Changes the bots activity status to "listening to ..."', inline=False)
#     embed.add_field(name='Watching', value='Changes the bots activity status to "watching ..."', inline=False)
#     embed.add_field(name='Competing in', value='Changes the bots activity status to "competing in ..."', inline=False)
#     embed.set_footer(text=f'{embed_footer}', icon_url=f'{embed_footer_icon}')
#     await ctx.send(embed=embed)
#     await ctx.message.add_reaction('👌')


# create a command that returns the creation date of a user, the roles, the avatar, and the discriminator
@bot.command(aliases=["uinfo", "ui", "uinf"], description="Usage: .userinfo", help="Information about the user")
async def userinfo(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.author
    embed = nextcord.Embed(title=f'{user.name}\'s info', color=0x00ff00)
    embed.set_thumbnail(url=f'{user.avatar.url}') 
    embed.add_field(name='Creation Date', value=f'{user.created_at.strftime("%d %b %Y %H:%M")}', inline=False)
    embed.add_field(name='Joined server', value=f'{user.joined_at.strftime("%d %b %Y %H:%M")}', inline=False)
    embed.add_field(name='Nickname', value=f'{user.nick}', inline=True)
    embed.add_field(name='UserID', value=f'{user.id}', inline=True)
    roles = " ".join([role.mention for role in user.roles if role.name != "@everyone"])
    # if roles is empty, then it will say that the user has no roles
    if roles == "":
        embed.add_field(name='Roles', value='None', inline=False)
    else:
        embed.add_field(name='Roles', value=f'{roles}', inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar)
    await ctx.send(embed=embed)


# create a roastme command that uses a random roast from a random category from the roastme.json file
@bot.command(description="Usage: .roastme", help="Yo Mama!")
async def roastme(ctx):
    try:
        with open('roastme.json', encoding="utf8") as f:
            data = json.load(f)
        category = random.choice(list(data.keys()))
        roast = random.choice(data[category])
        await ctx.send(f'{roast}')
    except Exception as e:
        await ctx.send(f'{e}')


# create a music command with the prefix .play using the youtube api
@bot.command(description="Usage: .music", help="Plays a song from youtube")
async def music(ctx, *, query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={(os.getenv("key"))}') as r:
                data = await r.json()
                embed = nextcord.Embed(title=f'Now Playing: {data["items"][0]["snippet"]["title"]}', color=0x00ff00)
                embed.set_thumbnail(url=f'{data["items"][0]["snippet"]["thumbnails"]["default"]["url"]}')
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
                await ctx.send(f'https://www.youtube.com/watch?v={data["items"][0]["id"]["videoId"]}')
                # bot joins voice channel of author
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                # bot plays the song from youtube
                source = FFmpegPCMAudio(f'https://www.youtube.com/watch?v={data["items"][0]["id"]["videoId"]}')
                # bot plays the song
                voice.play(source)
    except Exception as e:
        await ctx.send(f'{e}')











# MUSIC SHIT START

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data: data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


async def connect_to_voice_channel(ctx, channel):
    global voice_client, connected_to_vc
    voice_client = await channel.connect()
    if voice_client.is_connected():
        connected_to_vc = True
        await ctx.send(f'Connected to {voice_client.channel.name}')
    else:
        connected_to_vc = False
        await ctx.send(f'Failed to connect to voice channel {ctx.author.voice.channel.name}')


@bot.command()
async def disconnect(ctx):
    """Disconnect from voice channel"""
    global connected_to_vc, play_queue, player_obj_queue, current_server
    if connected_to_vc:
        await voice_client.disconnect()
        await ctx.send(f'Disconnected from {voice_client.channel.name}')
        connected_to_vc = False
        play_queue = []
        player_obj_queue = []
        current_server = None


@bot.command()
async def pause(ctx):
    """Pause the current song"""
    if connected_to_vc and voice_client.is_playing():
        voice_client.pause()
        await ctx.send('Paused')


@bot.command()
async def resume(ctx):
    """Resume the current song"""
    if connected_to_vc and voice_client.is_paused():
        voice_client.resume()
        await ctx.send('Resumed')


@bot.command()
async def skip(ctx):
    """Skip the current song"""
    if connected_to_vc and voice_client.is_playing():
        voice_client.stop()
        await play_next(ctx)


@bot.command()
async def queue(ctx):
    """Show the current queue"""
    if connected_to_vc:
        await ctx.send(f'{play_queue}')


@bot.command()
async def remove(ctx, id: int):
    """Remove an item from queue by index (1...)"""
    if connected_to_vc:
        if id == 0:
            await ctx.send('Cannot remove current playing song')
        else:
            await ctx.send(f'Removed {play_queue[id]}')
            play_queue.pop(id)
            player_obj_queue.pop(id)


@bot.command()
async def clq(ctx):
    """Clear the queue and stop current song"""
    global play_queue, player_obj_queue
    if connected_to_vc and voice_client.is_playing():
        voice_client.stop()
        play_queue = []
        player_obj_queue = []
        await ctx.send('Queue cleared.')


@bot.command()
async def song(ctx):
    """Show the current song"""
    if connected_to_vc:
        await ctx.send(f'Currently playing {play_queue[0]}')


async def play_next(ctx):
    print('\nPlaying next...')
    if play_queue:
        await play_song(ctx, player_obj_queue[0])
    else:
        await ctx.send('Reached end of queue')


def callback(e):
    if e:
        print(f'Error: {e}')
    else:
        # finished playing prev song without error so removing entry from queue here
        print('\nPlaying next...')
        if play_queue: play_queue.pop(0)
        if player_obj_queue:
            player_obj_queue.pop(0)
            voice_client.play(player_obj_queue[0], after=callback)
        else:
            print('Reached end of queue')


async def play_song(ctx, link):
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(link, loop=bot.loop, stream=False)
        except:
            print('Error encountered. Attempting to clear cache and retry...')
            subprocess.call('yt-dlp --rm-cache-dir', shell=True)
            player = await YTDLSource.from_url(link, loop=bot.loop, stream=False)
        player_obj_queue.append(player)
        if not voice_client.is_playing():
            voice_client.play(player_obj_queue[0], after=callback)
            await ctx.send(f'Now playing: {player_obj_queue[0].title}')


@bot.command()
async def play(ctx, *, song: str):
    """Play a YouTube video by URL if given a URL, or search up the song and play the first video in search result"""
    global connected_to_vc, current_server
    if current_server and current_server != ctx.guild:
        await ctx.send('The bot is currently being used in another server.')
        return
    elif current_server is None:
        current_server = ctx.guild
    if not connected_to_vc:
        if ctx.author.voice is None:
            connected_to_vc = False
            await ctx.send(f'You are not connected to any voice channel!')
        else:
            await connect_to_voice_channel(ctx, ctx.author.voice.channel)
    elif voice_client.channel != ctx.author.voice.channel:
        await voice_client.move_to(ctx.author.voice.channel)
    if connected_to_vc:
        try:
            requests.get(song)
        except (requests.ConnectionError, requests.exceptions.MissingSchema):
            URL = False
        else:
            URL = True
        if URL:
            link = song
        else:
            # Search up the query and play the first video in search result
            query_string = urllib.parse.urlencode({"search_query": song})
            formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
            search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
            link = f'https://www.youtube.com/watch?v={search_results[0]}'
        play_queue.append(link)
        if voice_client.is_playing():
            await ctx.send(f'Added to queue: {song}')
        await play_song(ctx, link)





























@bot.command(name="restart", aliases=["r", "reset"], description="Usage: .restart", help="Restarts the bot.")
async def restart(ctx):
    logs = bot.get_channel(791670764143247420)     #UM IN LOG CHANNEL ZU POSTEN
    restartembed = nextcord.Embed(
        title=f"{bot.user.name} is now restarting...",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    restartembed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar.url,
    )
    restartembed.set_footer(
        text=f"{embed_footer}",
        icon_url=f"{embed_footer_icon}"
    )
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        await ctx.message.add_reaction(clown5)
        await ctx.message.add_reaction(clown6)
        await ctx.message.add_reaction(clown7)
        await ctx.message.add_reaction(clown8)
        await ctx.message.add_reaction(clown9)
        return
        
    await logs.send(embed=restartembed)             #UM IN LOG CHANNEL ZU POSTEN
    # await ctx.send(embed=restartembed)              #UM IN DEN GLEICHEN CHANNEL ZU POSTEN

    await ctx.message.add_reaction("✅")
    await bot.close()



bot.run(os.getenv("TOKEN"))










# GANZ NETT MUSS ABER NICHT SEIN

# @bot.command()
# @has_permissions(ban_members=True)
# async def ban(ctx, member : nextcord.Member, *, reason = None):
#         await member.send(f"You have been banned in `{ctx.guild}`\nReason: `{reason}`") 
#         await member.ban(reason = reason)
#         await ctx.send(f"{member} has been successfully banned.") 