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
clown1 = '🤡'
clown2 = '<:literalclown:903780300839088188>'
clown3 = '<a:thumbsclown:931491107546738729>'
clown4 = '<:deadclown:931491107148300318>'
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."





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


# bot.remove_command('help')

# @bot.command()
# async def help(ctx):
#     await ctx.send("Not yet implemented")
#     return



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
        return

    if prefixset is None:
        prefixset = '.'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

        await ctx.send(f'The bots prefix has been reset to ``{prefixset}``')
        await ctx.message.add_reaction("✅")
        return

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

    if ctx.author.id == 399668151475765258:
        await ctx.channel.send('You got jebaited')





# REACTION TO EVERY MESSAGE FROM GIVEN USERID
# @bot.event
# async def on_message(message):
#     if message.author.id == 406456604825747466:       # Miranda
#         await message.add_reaction(clown1)
#         await ctx.message.add_reaction(clown2)
#         await ctx.message.add_reaction(clown3)
#         await ctx.message.add_reaction(clown4)

#     if message.author.id == 332945969492656129:       # ????
#         await message.add_reaction(clown1)
#         await ctx.message.add_reaction(clown2)
#         await ctx.message.add_reaction(clown3)
#         await ctx.message.add_reaction(clown4)

#     await bot.process_commands(message)






@bot.command(description='Usage: .mute [@USER]', help="TEMPORARILY DISABLED")
@has_permissions(manage_messages = True)
async def mute(ctx, member:nextcord.Member):
    if ctx.author.id != 399668151475765258:
        await ctx.channel.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
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
        return
    await ctx.channel.purge(limit=amount + 1)

    # if clear.amount.int == '*':
    #     await ctx.channel.purge()
    

@bot.command(aliases=['p'], description="Usage: .purge", help="Purges the whole channel")
async def purge(ctx ):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
        return
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






# BALLS (FOR ZARA)
@bot.command(aliases=["ball"], description="Usage: .balls", help="A command just for Zara")
async def balls(ctx):
    await ctx.message.add_reaction("<:balls:931483626913280000>")
    await ctx.message.add_reaction("<:caniholdyourballs:931486728173281320>")
    await ctx.message.add_reaction("<:therockraisedbrow:919887658661081088>")
    await ctx.message.add_reaction("<:idkbruh:931486728420724767>")
    await ctx.message.add_reaction("<a:spongepls:931486730517901357>")
    await ctx.message.add_reaction("<a:veryevil:931486730354303026>")
    await ctx.message.add_reaction("<:LETSGOOOOOOOOOO:931486729255419924>")







# **ONLINE**
@bot.command(description="Usage: .online", help="Changes the online status to online")
async def online(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
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
        return
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=2, name="your bullshit"))
    await ctx.message.add_reaction('🔴')

# **INVISIBLE**
@bot.command(aliases=["inv"], description="Usage: .invisible", help="Changes the online status to invisible")
async def invisible(ctx):
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(clown1)
        await ctx.message.add_reaction(clown2)
        await ctx.message.add_reaction(clown3)
        await ctx.message.add_reaction(clown4)
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
        return
    await bot.change_presence(activity=nextcord.Activity(type=5, name=message))
    await ctx.message.add_reaction('👌')
@compete.error
async def compete_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify the activity I should compete in')











































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