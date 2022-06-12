import asyncio
import os
import aiohttp
import random
import json
import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands.core import has_permissions
from nextcord.utils import get
from dotenv import load_dotenv


load_dotenv()

# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id="399668151475765258", case_insensitive=True)

# remove help command
bot.remove_command('help')


intents = nextcord.Intents().all()
intents.members = True
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."
perminv = "https://discord.com/api/oauth2/authorize?client_id=791670415779954698&permissions=137707659350&scope=bot"
dm_logs = "984869415684284536"





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





@bot.event
async def on_message(message: nextcord.Message):
    channel = bot.get_channel(984869415684284536)
    attachment = nextcord.Attachment
    if message.guild is not None:
        await bot.process_commands(message)
    if message.guild is None and not message.author.bot:
        await channel.send(f"<@!399668151475765258>\nNew message from {message.author.mention}:\nMessage content: `{message.content}`")
        await bot.process_commands(message)
        if isinstance(message.attachments, list):
            for attachment in message.attachments:
                if attachment.filename.endswith((".png", ".jpg", ".gif")):
                    await channel.send(f"{message.author.mention} sent a picture: {attachment.url}")
                    await bot.process_commands(message)
    




@bot.command()
async def dm(ctx, member: nextcord.Member, *, message):
    attachment = nextcord.Attachment
    if message == None:
        await ctx.message.delete()
        await member.send(f"{attachment}")
    else:
        await ctx.message.delete()
        await member.send(f"{message}")
        await ctx.send("DM sent :)")





# Changeprefix command
@bot.command(aliases=['setprefix'], description="Changes the prefix. If empty, resets the prefix to default.", help="Changes the prefix. If empty, resets the prefix to default.")
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





@bot.command(description='Make the bot say something in a specific channel', help="Make the bot say something in a specific channel")
async def say(ctx, channel: nextcord.TextChannel, *, message):
    # if ctx.author.id != 399668151475765258:
    #     await ctx.channel.send(f'{not_owner}')
    #     return
    await channel.send(f"{message}")





@bot.command(aliases=['em'], description="Embedded test message", help="Embedded test message")
async def embed(ctx, message = None, name = None, value = None):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
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
@bot.command(aliases=['claer', 'c'], description="Clears messages", help="Clears messages")
async def clear(ctx, amount : int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    await ctx.channel.purge(limit=amount + 1)

@bot.command(aliases=['p'], description="Purges the whole channel", help="Purges the whole channel")
async def purge(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await ctx.channel.purge()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete. Usage: `.clear [NUMBER]`')






# AVATAR COMMAND
@bot.command(aliases=["a", "av", "avtar", "avatr"], description="Displays a users avatar", help="Displays a users avatar")
async def avatar(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar.url

    avatarEmbed = nextcord.Embed(title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
    avatarEmbed.set_image(url=memberAvatar)
    avatarEmbed.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")

    await ctx.send(embed=avatarEmbed)








# **ONLINE**
@bot.command(description="Changes the online status to online", help="Changes the online status to online")
async def online(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.online,activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟢')

# **IDLE**
@bot.command(description="Changes the online status to idle", help="Changes the online status to idle")
async def idle(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🟡')

# **DO NOT DISTURB**
@bot.command(description="Changes the online status to dnd", help="Changes the online status to dnd")
async def dnd(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🔴')

# **INVISIBLE**
@bot.command(description="Changes the online status to invisible", help="Changes the online status to invisible")
async def invisible(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        return
    await bot.change_presence(status=nextcord.Status.invisible, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('⚪')





# PLAYING
@bot.command(description="Changes the bots activity status to 'playing ...'", help="Changes the bots activity status to 'playing ...'")
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
@bot.command(description="Changes the bots activity status to 'listening to ...'", help="Changes the bots activity status to 'listening to ...'")
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
@bot.command(description="Changes the bots activity status to 'watching ...'", help="Changes the bots activity status to 'watching ...'")
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
@bot.command(description="Changes the bots activity status to 'competing in ...'", help="Changes the bots activity status to 'competing in ...'")
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





@bot.command(description="Usage: .ping", help="Returns the bots latency")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    await ctx.message.add_reaction('👌')




@bot.event
async def on_message_delete(message):
    if message.guild.id == 791670762859266078:
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(title='Message Deleted', description=f'{message.author.mention} deleted the message: {message.content}\n In the channel {message.channel.mention}', color=0x00ff00)
        embed.set_footer(text=f'{message.author}', icon_url=message.author.display_avatar)
        await channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if before.guild.id == 791670762859266078:
        if before.author.bot:
            return
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(title='Message Edited', description=f'{before.author.mention} edited the message: ```{before.content}``` to\n ```{after.content}```', color=0x00ff00)
        embed.set_footer(text=f'{before.author}', icon_url=before.author.display_avatar)
        await channel.send(embed=embed)


@bot.command(description="Posts a random dog picture from the dog api", help="Posts a random dog picture from the dog api")
async def dog(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                await ctx.send(data['message'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(description="Posts a random cat picture from the cat api", help="Posts a random cat picture from the cat api") # 
async def cat(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                data = await r.json()
                await ctx.send(data['file'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(aliases=["inv"], description="Sends the bots invite link", help="Sends the bots invite link")
async def invite(ctx):
    await ctx.send(f'{perminv}')


@bot.command(description="Posts a random meme from the dankmemes and memes subreddit", help="Posts a random meme from the dankmemes and memes subreddit")
async def meme(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')


@bot.command(aliases=["uinfo", "ui", "uinf"], description="Information about the user", help="Information about the user")
async def userinfo(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.author
    embed = nextcord.Embed(title=f'{user.name}\'s info', color=0x00ff00)
    embed.set_thumbnail(
        url=f'{user.avatar.url}'
        )
    embed.add_field(
        name='Creation Date', 
        value=f'{user.created_at.strftime("%d %b %Y %H:%M")}', 
        inline=True
    )
    embed.add_field(
        name='Joined server', 
        value=f'{user.joined_at.strftime("%d %b %Y %H:%M")}', 
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





@bot.command(description="Yo Mama!", help="Yo Mama!")
async def roastme(ctx):
    try:
        with open('roastme.json', encoding="utf8") as f:
            data = json.load(f)
        category = random.choice(list(data.keys()))
        roast = random.choice(data[category])
        await ctx.send(f'{roast}')
    except Exception as e:
        await ctx.send(f'{e}')





@bot.command(description="Posts a random image from the nsfw subreddit", help="Posts a random image from the nsfw subreddit")
async def nsfw(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/nsfw/random.json') as r:
                data = await r.json()
                await ctx.send(data[0]['data']['children'][0]['data']['url'])
    except Exception as e:
        await ctx.send(f'{e}')





@bot.command()
async def hentai(ctx, *, search):
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
        await ctx.reply("Please provide an endpoint. Use `!hentai list` to see all the tags")





@bot.command()
async def reminder(ctx, time, *, reminder):
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
@bot.command(description="Kicks a user", help="Kicks a user")
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


@bot.command(description="Bans a user", help="Bans a user")
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

@bot.command(description="Unbans a user", help="Unbans a user")
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





@bot.command()
async def blind(ctx, member: nextcord.Member, role = None):
    if member == ctx.author:
        await ctx.reply("You can't blind yourself, idiot. *Who hired this guy?*")
        return
    if (not ctx.author.guild_permissions.manage_roles):
        await ctx.reply(f'{missing_perms}')
        return
    role = ctx.guild.get_role(984816627746996305)
    await member.edit(roles=[role])















@bot.command(description="Shows this message", help="Shows this message")
async def help(ctx):
    embed = nextcord.Embed(title="Pluto help", color=0x00ff00)
    for command in bot.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(name=f"`{command.name}{command.signature if command.signature is not None else''}`", value=description)
    await ctx.send(embed=embed)





@bot.command(aliases=["r", "reset"], description="Restarts the bot.", help="Restarts the bot.")
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



bot.run(os.getenv("TOKEN"))