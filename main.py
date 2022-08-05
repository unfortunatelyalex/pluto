import os
import pytz
import json
import random
import asyncio
import aiohttp
import requests
import datetime
import nextcord
from utils import *
from nextcord.utils import get
from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord.ext.commands import MissingRequiredArgument
from nextcord import Intents, Interaction, SlashOption, ChannelType, ButtonStyle


load_dotenv()

# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = nextcord.Intents.default()
intents.message_content = True
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."
perminv = os.getenv("botinv")
dm_logs = "984869415684284536"



# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id="399668151475765258", case_insensitive=True, intents=intents)
bot.remove_command('help')

bot.lavalink_nodes = [
    {"host": "lava.link", "port": 80, "password": "dismusic"},
]

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
    bot.load_extension('dismusic')
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
        embed = nextcord.Embed(title='Message Deleted', description=f'{message.author.mention} deleted the message: {message.content}\n In the channel {message.channel.mention}', color=0x00ff00)
        embed.set_footer(text=f'{message.author}', icon_url=message.author.display_avatar)
        await channel.send(embed=embed)

# Edited message log
@bot.event
async def on_message_edit(before, after):
    if before.guild.id == 791670762859266078:
        if before.author.bot:
            return
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(title='Message Edited', description=f'{before.author.mention} edited the message: ```{before.content}``` to\n ```{after.content}```', color=0x00ff00)
        embed.set_footer(text=f'{before.author}', icon_url=before.author.display_avatar)
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
        await ctx.send(f"{missing_perms}")
        return
    if ctx.author.id != 399668151475765258:
        embed = nextcord.Embed(title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(text=f"This message was sent by {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.message.delete()
        await member.send(embed=embed)
        return
        
    else:
        embed = nextcord.Embed(title=f"hello {member.name}!", description=f"{message}", color=0x00ff00)
        embed.set_footer(text="This message was sent anonymously", icon_url=f"{embed_footer_icon}")
        await ctx.message.delete()
        await member.send(embed=embed)
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
    # if ctx.author.id != 399668151475765258:
    #     await ctx.channel.send(f'{not_owner}')
    #     return
    # delete the command message
    await ctx.message.delete()
    await channel.send(f"{message}")





# CLEAR MESSAGES COMMAND
@bot.command(aliases=['claer', 'c'], description="Clears messages", help=".clear <amount>")
async def clear(ctx, amount : int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    await ctx.channel.purge(limit=amount + 1)

@bot.command(description="Purges the whole channel", help=".purge")
async def purge(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await ctx.channel.purge()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete. Usage: `.clear [NUMBER]`')





@bot.command(aliases=['uclear', 'uc'], description="Kicks a user from the server", help=".kick <user>")
async def userclear(ctx, member: nextcord.Member, amount: int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    # only clear messages from the mentioned user
    await ctx.channel.purge(limit=amount + 1, check=lambda m: m.author == member)






# AVATAR COMMAND
@bot.command(aliases=["a", "av", "avtar", "avatr"], description="Displays a users avatar", help=".avatar <user>")
async def avatar(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar.url

    avatarEmbed = nextcord.Embed(title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatarEmbed.set_image(url=memberAvatar)
    avatarEmbed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")

    await ctx.send(embed=avatarEmbed)








# **ONLINE**
@bot.command(description="Changes the online status to online", help=".online")
async def online(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.online,activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟢')

# **IDLE**
@bot.command(description="Changes the online status to idle", help=".idle")
async def idle(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟡')

# **DO NOT DISTURB**
@bot.command(description="Changes the online status to dnd", help=".dnd")
async def dnd(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🔴')

# **INVISIBLE**
@bot.command(description="Changes the online status to invisible", help=".invisible")
async def invisible(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.invisible, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('⚪')





# PLAYING
@bot.command(description="Changes the bots activity status to 'playing ...'", help=".playing <activity>")
async def playing(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(activity=nextcord.Activity(type=0, name=message))
    await ctx.message.add_reaction('👌')
@playing.error
async def playing_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what game I should play.')


# LISTENING TO
@bot.command(description="Changes the bots activity status to 'listening to ...'", help=".listening <activity>")
async def listening(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(activity=nextcord.Activity(type=2, name=message))
    await ctx.message.add_reaction('👌')
@listening.error
async def listening_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what song I should listen to.')


# WATCHING
@bot.command(description="Changes the bots activity status to 'watching ...'", help=".watching <activity>")
async def watching(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(activity=nextcord.Activity(type=3, name=message))
    await ctx.message.add_reaction('👌')
@watching.error
async def watching_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify what video I should watch.')


# COMPETING IN
@bot.command(description="Changes the bots activity status to 'competing in ...'", help=".compete <activity>")
async def compete(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(activity=nextcord.Activity(type=5, name=message))
    await ctx.message.add_reaction('👌')
@compete.error
async def compete_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify the activity I should compete in')





@bot.command(description="Returns the bot's ping", help=".ping")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.message.add_reaction('👌')





@bot.command(description="Posts a random dog picture from the dog api", help=".dog")
async def dog(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                await ctx.send(data['message'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(description="Posts a random cat picture from the cat api", help=".cat")
async def cat(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                data = await r.json()
                await ctx.send(data['file'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(aliases=["inv"], description="Sends the bots invite link", help=".invite")
async def invite(ctx):
    await ctx.send("pluto isn't public, stfu")


@bot.command(description="Posts a random meme from the dankmemes subreddit", help=".meme")
async def meme(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(aliases=["uinfo", "ui", "uinf"], description="Information about the user", help=".userinfo <user>")
async def userinfo(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.author
    embed = nextcord.Embed(title=f'{user.name}\'s info', color=0x00ff00)
    embed.set_thumbnail(
        url=f'{user.avatar.url}'
        )
    embed.add_field(
        name='Creation Date', 
        value=f'{user.created_at.strftime("%d %b %Y %H:%M:%S")}', 
        inline=True
    )
    embed.add_field(
        name='Joined server', 
        value=f'{user.joined_at.strftime("%d %b %Y %H:%M:%S")}', 
        inline=True
    )
    embed.add_field(
        name="‎ ", 
        value="‎ ", 
        inline=True
    )
    embed.add_field(
        name='Full name', 
        value=f'{user.mention}', 
        inline=True
    )
    embed.add_field(
        name='Nick', 
        value=f'{user.nick}', 

        inline=True
    )
    embed.add_field(
        name='UserID', 
        value=f'{user.id}', 
        inline=False
    )
    roles = " ".join([role.mention for role in user.roles if role.name != "@everyone"])
    if roles == "":
        embed.add_field(
            name='Roles', 
            value='None', 
            inline=True
        )
    else:
        embed.add_field(
            name='Roles', 
            value=f'{roles}', 
            inline=True
        )
    embed.set_footer(
        text=f'Requested by {ctx.author}', 
        icon_url=ctx.author.avatar.url
    )
    await ctx.send(embed=embed)





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





@bot.command(description="Posts a random image from the nsfw subreddit", help=".nsfw")
async def nsfw(ctx):
    # if the command doesn't get sent in a nsfw channel, it will send a message saying so
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





@bot.command(description="Let pluto remind you of something", help=".remind <time> <reminder>")
async def remind(ctx, time, *, reminder):
    print(time)
    print(reminder)
    embed = nextcord.Embed(color=0x55a7f7, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
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
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about `{reminder}` in `{counter}`.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hello {ctx.author.mention}, you asked me to remind you about `{reminder}` `{counter}` ago.")
        return
    await ctx.send(embed=embed)




# MODERATION
@bot.command(description="Kicks a user", help=".kick <user> <reason>")
async def kick(ctx, member : nextcord.Member, *, reason = None):
    if member == ctx.author:
        await ctx.reply("You can't kick yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.reply(f'{missing_perms}')
        return
    if reason is None:
        await ctx.reply("You need to specify a reason to kick this user")
        return
    await member.send(f"You have been kicked in `{ctx.guild}`\nReason: `{reason}`")
    await member.kick(reason = reason)
    await ctx.send(f"{member} has been successfully kicked.")
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to kick.")
            return


@bot.command(description="Bans a user", help=".ban <user> <reason>")
async def ban(ctx, member : nextcord.Member, *, reason = None):
    if member == ctx.author:
        await ctx.reply("You can't ban yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.reply(f'{missing_perms}')
        return
    if reason is None:
        await ctx.reply("You need to specify a reason to ban this user")
        return
    
    await ctx.send(f"{member} has been successfully banned.")
    await member.send(f"You have been banned in `{ctx.guild}`\nReason: `{reason}`")
    async with member.typing():
        await asyncio.sleep(3)
    await member.send("You fucking idiot must've pissed alex off really bad if he banned you")
    await member.ban(reason = reason)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to ban.")
            return

@bot.command(description="Unbans a user", help=".unban <user>")
async def unban(ctx, *, member):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.reply(f'{missing_perms}')
        return
    if "#" in ctx.message.content:
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users: 
                member_name, member_discriminator = member.split('#')
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"{user} has been successfully unbanned.")
        return
    else:
        member = await bot.fetch_user(int(member))
        await ctx.guild.unban(member)
        await ctx.send(f"{user} has been successfully unbanned.")
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to unban.")
            return





@bot.command(description="Blind the user, making him unable to see other channels", help=".blind <user>")
async def blind(ctx, member: nextcord.Member):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    if member == ctx.author:
        await ctx.reply("You can't blind yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.manage_roles):
        await ctx.reply(f'{missing_perms}')
        return
    role = ctx.guild.get_role(984816627746996305)
    await member.edit(roles=[role])
    
@blind.error
async def blind_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        if error.param.name == "member":
            await ctx.reply("You need to specify a member to blind.")
            return





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
    engines = int(stats['malicious']) + int(stats['undetected']) + int(stats['harmless'])
    scans = scanresult['results']

    ismalw = ':warning: marked as malicious'
    color = 0xf58f14

    trusted_engines_detect = False
    try:
        trusted_engines_detect = (
            (scans['Dr.Web']['result'] != 'clean' and scans['Dr.Web']['result'] != None) or \
            (scans['DrWeb']['result'] != 'clean' and scans['DrWeb']['result'] != None) or \
            (scans['BitDefender']['result'] != 'clean' and scans['BitDefender']['result'] != None)
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
    resultmsg = nextcord.Embed(color=color, title=f'The {scantype} is {ismalw} ({stats["malicious"]}/{engines})', description=resultstr)
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
            await move_lobby.set_permissions(after.channel.guild.default_role, view_channel=False, connect=False)

            if channel is not None:
                await member.move_to(channel)

    if before.channel is not None:
        if before.channel.category.id == get_category_by_name(before.channel.guild, "idek").id:
            # set move_lobby as a variable to avoid errors
            move_lobby = get_channel_by_name(before.channel.guild, f"⬆ {member.name} Lobby".lower())

            # check if a voice channel in tempchannel.json is empty, if so, delete it 
            with open("tempchannel.json", "r") as f:
                data = json.load(f)
            if data[f"{member.name}".lower()] is not None:
                channel = get(before.channel.guild.channels, id=data[f"{member.name}".lower()])
                if channel is not None:
                    if len(channel.members) == 0:
                        await channel.delete()
                        await move_lobby.delete()
                        # delete both channels from the file
                        data[f"{member.name}".lower()] = None
                        data[f"{member.name}".lower() + "lobby"] = None
                        with open("tempchannel.json", "w") as f:
                            json.dump(data, f, indent=4)









@bot.group(invoke_without_command=True)
async def help(ctx):
    timezone = pytz.timezone('CET')
    time = datetime.datetime.now(timezone)
    await ctx.send(
        f"""
> **Commands**
> 
> ```ansi
> [35m<>[0m is required | [34m[][0m is optional
> ``````ansi
> For more information on a command
> .help [35m<command>[0m
> ``````ansi
> Commands
> 
> .avatar [34m[user][0m              » Shows the avatar of the user
> .cat                        » Shows a random cat image
> .dog                        » Shows a random dog image
> .hentai [35m<endpoint>[0m          » It's hentai...
> .meme                       » Sends a random meme
> .nsfw                       » Sends a random nsfw image/gif
> .ping                       » Pong!
> .prefix [35m<newprefix>[0m         » Sets a new prefix
> .remind [35m<time> <reminder>[0m   » Let pluto remind you of something
> .roastme                    » Yo Mama!
> .scan [35m[attachment][0m          » Scans a file with VirusTotal 
> .userinfo [34m[user][0m            » Gives info about a user
> ``````ansi
> Requested by {ctx.author.name} at {time.strftime('%H:%M:%S')} CET
> ```
"""
    )

# UNTER HENTAI!!!!!!  > .invite                     » Sends the bot invite link



@help.command(name="avatar")
async def avatar_sub(ctx):
    avatar = nextcord.Embed(title="What does he look like", description="Shows the avatar of the user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    avatar.add_field(name="**Usage:**", value="{p}avatar <user/if none, you>")
    avatar.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=avatar)

@help.command(name="cat")
async def cat_sub(ctx):
    cat = nextcord.Embed(title="Meow", description="Posts a cat image from a Cat API",timestamp=datetime.datetime.now(datetime.timezone.utc))
    cat.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    cat.add_field(name="**Usage:**", value="{p}cat")
    cat.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=cat)

@help.command(name="dog")
async def dog_sub(ctx):
    dog = nextcord.Embed(title="Woof", description="Posts a dog image from a Dog API",timestamp=datetime.datetime.now(datetime.timezone.utc))
    dog.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    dog.add_field(name="**Usage:**", value="{p}dog")
    dog.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=dog)

@help.command(name="help")
async def help_sub(ctx):
    help = nextcord.Embed(title="<:6682imdead:948990530241572915>", description="Well...this is awkward",timestamp=datetime.datetime.now(datetime.timezone.utc))
    help.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    help.add_field(name="?????", value="Why would you need help with the help command?!")
    help.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=help)

@help.command(name="hentai")
async def hentai_sub(ctx):
    hentai = nextcord.Embed(title="Anime but lewd", description="Posts hentai <:sadge:985124366561980476>",timestamp=datetime.datetime.now(datetime.timezone.utc))
    hentai.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    hentai.add_field(name="**Usage:**", value="{p}hentai <endpoint>")
    hentai.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=hentai)

# @help.command(name="invite")
# async def invite_sub(ctx):
#     invite = nextcord.Embed(title="I can follow you", description="Sends an invite link to the bot",timestamp=datetime.datetime.now(datetime.timezone.utc))
#     invite.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
#     invite.add_field(name="**Usage:**", value="{p}invite")
#     invite.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
#     await ctx.reply(embed=invite)

@help.command(name="meme")
async def meme_sub(ctx):
    meme = nextcord.Embed(title="Why yes, of course I enjoy memes", description="Posts a meme from a Meme API",timestamp=datetime.datetime.now(datetime.timezone.utc))
    meme.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    meme.add_field(name="**Usage:**", value="{p}meme")
    meme.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=meme)

@help.command(name="nsfw")
async def nsfw_sub(ctx):
    nsfw = nextcord.Embed(title="Porn...regular porn", description="Posts an image or video from the nsfw subreddit",timestamp=datetime.datetime.now(datetime.timezone.utc))
    nsfw.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    nsfw.add_field(name="**Usage:**", value="{p}nsfw")
    nsfw.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=nsfw)

@help.command(name="ping")
async def ping_sub(ctx):
    ping = nextcord.Embed(title="I don't like this game", description="Pings the bot",timestamp=datetime.datetime.now(datetime.timezone.utc))
    ping.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    ping.add_field(name="**Usage:**", value="{p}ping")
    ping.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=ping)

@help.command(name="prefix")
async def prefix_sub(ctx):
    prefix = nextcord.Embed(title="mMMmmm prefix", description="Sets a new prefix for the bot",timestamp=datetime.datetime.now(datetime.timezone.utc))
    prefix.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    prefix.add_field(name="**Usage:**", value="{p}prefix <new prefix>")
    prefix.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=prefix)

@help.command(name="remind")
async def remind_sub(ctx):
    remind = nextcord.Embed(title="Do you have alzheimers", description="Sets a reminder for you",timestamp=datetime.datetime.now(datetime.timezone.utc))
    remind.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    remind.add_field(name="**Usage:**", value="{p}remind <time> <message>")
    remind.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=remind)

@help.command(name="roastme")
async def roastme_sub(ctx):
    roastme = nextcord.Embed(title="Yo Mama!", description="Roasts you",timestamp=datetime.datetime.now(datetime.timezone.utc))
    roastme.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    roastme.add_field(name="**Usage:**", value="{p}roastme")
    roastme.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=roastme)

@help.command(name="scan")
async def scan_sub(ctx):
    scan = nextcord.Embed(title="I don't trust this image of a fork", description="Scan a file with Virustotal",timestamp=datetime.datetime.now(datetime.timezone.utc))
    scan.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    scan.add_field(name="**Usage:**", value="{p}scan [attachment]")
    scan.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=scan)

@help.command(name="userinfo")
async def userinfo_sub(ctx):
    userinfo = nextcord.Embed(title="Let's stalk this guy", description="Gives information about a user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    userinfo.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    userinfo.add_field(name="**Usage:**", value="{p}userinfo <user/if none, you>")
    userinfo.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=userinfo)








@bot.group(invoke_without_command=True)
async def adminhelp(ctx):
    if ctx.author.guild_permissions.administrator == False:
        await ctx.reply(f"{missing_perms}")
        return
    timezone = pytz.timezone('CET')
    time = datetime.datetime.now(timezone)

    await ctx.send(
        f"""
> **Admin Commands**
> 
> ```ansi
> [35m<>[0m is required | [34m[][0m is optional
> ``````ansi
> For more information on a command
> .adminhelp [35m<command>[0m
> ``````ansi
> Commands
> 
> .ban [35m<user> <reason>[0m     » Ban a user
> .blind [35m<user>[0m            » Adds the 'blind' role to the user
> .clear [35m<amount>[0m          » Clears the chat
> .compete [35m<activity>[0m      » Activity status to "Competing in..."
> .dm [35m<user> <message>[0m     » Sends a DM to a user
> .dnd                     » Online Status to "Do Not Disturb"
> .idle                    » Online Status to "Idle"
> .invisible               » Online Status to "Invisible"
> .kick [35m<user> <reason>[0m    » Kick a user
> .listening [35m<activity>[0m    » Activity status to "Listening to..."
> .online                  » Online Status to "Online"
> .playing [35m<activity>[0m      » Activity status to "Playing..."
> .purge                   » Purges the whole channel
> .restart                 » Restarts the bot
> .say [35m<channel> <message>[0m » Sends a message to a channel
> .unban [35m<user>[0m            » Unban a user
> .watching [35m<activity>[0m     » Activity status to "Watching..."
> ``````ansi
> Requested by {ctx.author.name} at {time.strftime('%H:%M:%S')} CET 
> ```
"""
    )


@adminhelp.command(name="ban")
async def ban_sub(ctx):
    ban = nextcord.Embed(title="Bad people must be punished", description="Bans the user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    ban.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    ban.add_field(name="**Usage:**", value="{p}ban <user> <reason>")
    ban.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=ban)

@adminhelp.command(name="blind")
async def blind_sub(ctx):
    blind = nextcord.Embed(title="Flashbang!!!", description="Adds the 'blind' role to the user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    blind.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    blind.add_field(name="**Usage:**", value="{p}blind <user>")
    blind.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=blind)

@adminhelp.command(name="clear")
async def clear_sub(ctx):
    clear = nextcord.Embed(title="You saw nothing", description="Clears the amount of messages you specify",timestamp=datetime.datetime.now(datetime.timezone.utc))
    clear.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    clear.add_field(name="**Usage:**", value="{p}clear <amount>")
    clear.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=clear)

@adminhelp.command(name="compete")
async def compete_sub(ctx):
    compete = nextcord.Embed(title="Gotta compete in something", description="Competes in the specified game",timestamp=datetime.datetime.now(datetime.timezone.utc))
    compete.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    compete.add_field(name="**Usage:**", value="{p}compete <activity>")
    compete.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=compete)

@adminhelp.command(name="dm")
async def dm_sub(ctx):
    dm = nextcord.Embed(title="Hello Human", description="Sends a DM to the user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    dm.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    dm.add_field(name="**Usage:**", value="{p}dm <user> <message>")
    dm.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=dm)

@adminhelp.command(name="dnd")
async def dnd_sub(ctx):
    dnd = nextcord.Embed(title="Don't annoy me", description="Sets the online status of pluto to 'Do Not Disturb'",timestamp=datetime.datetime.now(datetime.timezone.utc))
    dnd.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    dnd.add_field(name="**Usage:**", value="{p}dnd <user>")
    dnd.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=dnd)

@adminhelp.command(name="idle")
async def idle_sub(ctx):
    idle = nextcord.Embed(title="I'm actually not there", description="Sets the online status of pluto to 'Idle'",timestamp=datetime.datetime.now(datetime.timezone.utc))
    idle.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    idle.add_field(name="**Usage:**", value="{p}idle")
    idle.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=idle)

@adminhelp.command(name="invisible")
async def invisible_sub(ctx):
    invisible = nextcord.Embed(title="oOoOooOooO I'm a ghost", description="Sets the online status of pluto to 'Invisible'",timestamp=datetime.datetime.now(datetime.timezone.utc))
    invisible.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    invisible.add_field(name="**Usage:**", value="{p}invisible")
    invisible.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=invisible)

@adminhelp.command(name="kick")
async def kick_sub(ctx):
    kick = nextcord.Embed(title="Boot in your butt", description="Kicks the specified user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    kick.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    kick.add_field(name="**Usage:**", value="{p}kick <user>")
    kick.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=kick)

@adminhelp.command(name="listening")
async def listening_sub(ctx):
    listening = nextcord.Embed(title="What are you listening to", description="Listens to an imaginary song",timestamp=datetime.datetime.now(datetime.timezone.utc))
    listening.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    listening.add_field(name="**Usage:**", value="{p}listening <activity>")
    listening.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=listening)

@adminhelp.command(name="online")
async def online_sub(ctx):
    online = nextcord.Embed(title="Yes, here, I'm here, hello!", description="Sets the online status of pluto to 'Online'",timestamp=datetime.datetime.now(datetime.timezone.utc))
    online.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    online.add_field(name="**Usage:**", value="{p}online")
    online.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=online)

@adminhelp.command(name="playing")
async def playing_sub(ctx):
    playing = nextcord.Embed(title="You got any games on your phone", description="Plays an imaginary game",timestamp=datetime.datetime.now(datetime.timezone.utc))
    playing.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    playing.add_field(name="**Usage:**", value="{p}playing <activity>")
    playing.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=playing)

@adminhelp.command(name="purge")
async def purge_sub(ctx):
    purge = nextcord.Embed(title="Thanos snap this channel", description="Deletes the whole chat",timestamp=datetime.datetime.now(datetime.timezone.utc))
    purge.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    purge.add_field(name="**Usage:**", value="{p}purge")
    purge.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=purge)

@adminhelp.command(name="restart")
async def restart_sub(ctx):
    restart = nextcord.Embed(title="Let's try this again", description="Restarts the bot",timestamp=datetime.datetime.now(datetime.timezone.utc))
    restart.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    restart.add_field(name="**Usage:**", value="{p}restart")
    restart.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=restart)

@adminhelp.command(name="say")
async def say_sub(ctx):
    say = nextcord.Embed(title="I can be Human too", description="Make the bot say something in a specific channel",timestamp=datetime.datetime.now(datetime.timezone.utc))
    say.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    say.add_field(name="**Usage:**", value="{p}say <channel> <message>")
    say.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=say)

@adminhelp.command(name="unban")
async def unban_sub(ctx):
    unban = nextcord.Embed(title="I forgive you", description="Unbans a user",timestamp=datetime.datetime.now(datetime.timezone.utc))
    unban.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    unban.add_field(name="**Usage:**", value="{p}unban <user>")
    unban.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=unban)

@adminhelp.command(name="watching")
async def watching_sub(ctx):
    watching = nextcord.Embed(title="YouTube...hmmmm", description="Watch an imaginary video",timestamp=datetime.datetime.now(datetime.timezone.utc))
    watching.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    watching.add_field(name="**Usage:**", value="{p}watching <activity>")
    watching.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.reply(embed=watching)









@bot.command(aliases=["r", "reset"], description="Restarts the bot.", help=".restart")
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
        return
        
    await logs.send(embed=restartembed)             #UM IN LOG CHANNEL ZU POSTEN
    # await ctx.send(embed=restartembed)              #UM IN DEN GLEICHEN CHANNEL ZU POSTEN

    await ctx.message.add_reaction("✅")
    await bot.close()










# Elias ersatz

@bot.command(description="Self roles")
async def rr(ctx):

    # if author doesn't have admin permissions, return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permissions to send this command", delete_after=3)
        return

    young = Button(label="13-15", style=ButtonStyle.blurple)
    young_role = nextcord.utils.get(ctx.guild.roles,name="13-15")

    middle = Button(label="15-17", style=ButtonStyle.blurple)
    middle_role = nextcord.utils.get(ctx.guild.roles,name="15-17")

    old = Button(label="18+", style=ButtonStyle.blurple)
    old_role = nextcord.utils.get(ctx.guild.roles,name="18+😳")

    man = Button(label="Männlich", style=ButtonStyle.blurple)
    man_role = nextcord.utils.get(ctx.guild.roles,name="Männlich")

    girl = Button(label="Weiblich", style=ButtonStyle.blurple)
    girl_role = nextcord.utils.get(ctx.guild.roles,name="Weiblich")

    divers = Button(label="Divers", style=ButtonStyle.red)
    divers_role = nextcord.utils.get(ctx.guild.roles,name="Divers")

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

    embed = nextcord.Embed(title="Reaction Roles", description="Click on the buttons to get your roles")
    embed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await ctx.message.delete()
    await ctx.send(embed=embed, view=buttonsxd)








if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))