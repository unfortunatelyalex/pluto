import os
import nextcord
import random
import json
import datetime
import logging
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands.core import has_permissions
from dotenv import load_dotenv

# LOG
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
logger.addHandler(handler)


load_dotenv()

# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id="399668151475765258", case_insensitive=True)

intents = nextcord.Intents().all()
intents.members = True
emoji = '🤡'
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\n(MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\n(NotOwner)\nIf you believe this could be a mistake, please contact your administrator."





# Ready up message and activity status
@bot.event
async def on_ready():
    print('--------------------------------')
    print(f"     Logged in as {bot.user} ")
    print(f" User-ID = {bot.user.id}")
    print(f"            {nextcord.__version__}")
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
        return

    if prefixset is None:
        prefixset = '.'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'The bot prefix has been changed to ``{prefixset}``')





# Token command
@bot.command(aliases=['key', 'api', 'apikey'], description='Usage: .token', help="Shows the Token of this Bot")
async def token(message):
    if message.author.id != 399668151475765258:
        await message.channel.send(f'{missing_perms}')

    if message.author.id == 399668151475765258:
        await message.channel.send('You got jebaited')





# REACTION TO EVERY MESSAGE FROM GIVEN USERID
@bot.event
async def on_message(message):
    if message.author.id == 406456604825747466:
        await message.add_reaction(emoji)

    if message.author.id == 332945969492656129:
        await message.add_reaction(emoji)

    await bot.process_commands(message)






@bot.command(pass_context=True)
@has_permissions(manage_messages = True)
async def mute(ctx, member:nextcord.Member):
    role = nextcord.utils.get(ctx.guild.roles, name='Mommy')
    await member.add_roles(role)

@bot.command(pass_context=True)
@has_permissions(manage_messages = True)
async def unmute(ctx, member:nextcord.Member):
    role = nextcord.utils.get(ctx.guild.roles, name='Mommy')
    await member.remove_roles(role)






@bot.command()
async def say(ctx, channel: nextcord.TextChannel, *, message):
		await channel.send(f"{message}")







@bot.command(pass_context=True, aliases=['em'], description="Usage: .embed [YOUR TEST TEXT]", help="Embedded test message")
async def embed(ctx, *, message = None):
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
        name="text1",
        value="textvalue1"
    )
    await ctx.send(embed=embed)





# CLEAR MESSAGES COMMAND
@bot.command(aliases=['claer', 'c'], description="Usage: .clear [Amount of messages you want to delete]", help="Clears messages")
async def clear(ctx, amount : int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    await ctx.channel.purge(limit=amount + 1)

    # if clear.amount.int == '*':
    #     await ctx.channel.purge()
    

@bot.command(aliases=['p'], description="Usage: .purge", help="Purges the whole channel")
async def purge(ctx ):
  await ctx.channel.purge()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete')






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





# COMMANDS COMMAND
@bot.command(name="commands", description="Usage: .commands", help="Lists every command available")
async def commands(ctx):
    commands = "```"
    for command in bot.commands:
        commands += f"{command}\n"
    commands += "```"
    await ctx.send(commands)





# **ONLINE**
@bot.command(description="Usage: .online", help="Changes the online status to online")
async def online(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(emoji)
        return
    await bot.change_presence(status=nextcord.Status.online,activity=nextcord.Activity(type=5, name="your bullshit"))
    await ctx.message.add_reaction('🟢')

# **IDLE**
@bot.command(description="Usage: .idle", help="Changes the online status to idle")
async def idle(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(emoji)
        return
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=5, name="your bullshit"))
    await ctx.message.add_reaction('🟡')

# **DO NOT DISTURB**
@bot.command(description="Usage: .dnd", help="Changes the online status to dnd")
async def dnd(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(emoji)
        return
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=5, name="your bullshit"))
    await ctx.message.add_reaction('🛑')





# PLAYING
@bot.command(description="Usage: .playing [GAME]", help="Changes the bots activity status to 'playing ...'")
async def playing(ctx, *, message):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(emoji)
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
        await ctx.message.add_reaction(emoji)
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
        await ctx.message.add_reaction(emoji)
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
        await ctx.message.add_reaction(emoji)
        return
    await bot.change_presence(activity=nextcord.Activity(type=5, name=message))
    await ctx.message.add_reaction('👌')
@compete.error
async def compete_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify the activity I should compete in')








@bot.command(pass_context=True, name="restart", aliases=["r", "reset"], description="Usage: .restart", help="Restarts the bot.")
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
        await ctx.message.add_reaction(emoji)
        return
        
    await logs.send(embed=restartembed)             #UM IN LOG CHANNEL ZU POSTEN
    # await ctx.send(embed=restartembed)              #UM IN DEN GLEICHEN CHANNEL ZU POSTEN

    await ctx.message.add_reaction("✅")
    await bot.close()



bot.run(os.getenv("TOKEN"))










# GANZ NETT MUSS ABER NICHT SEIN

# @bot.command(pass_context=True)
# @has_permissions(ban_members=True)
# async def ban(ctx, member : nextcord.Member, *, reason = None):
#         await member.send(f"You have been banned in `{ctx.guild}`\nReason: `{reason}`") 
#         await member.ban(reason = reason)
#         await ctx.send(f"{member} has been successfully banned.") 