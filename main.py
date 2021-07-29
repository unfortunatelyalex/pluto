import os
import discord
import random
import json
import datetime
from discord.ext import commands
from discord.ext.commands.core import is_owner
from dotenv import load_dotenv

load_dotenv()

# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Getting Prefix
bot = commands.Bot(command_prefix=get_prefix, owner_id = 399668151475765258, case_insensitive=True)

intents = discord.Intents().all()
intents.members = True
emoji = '🤡'
embed_footer = 'made with 💛 by alex.#6247'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\n(MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\n(NotOwner)\nIf you believe this could be a mistake, please contact your administrator."





# Ready up message and activity status
@bot.event
async def on_ready():
    print('------')
    print(f"Logged in as {bot.user} ")
    print(f"User-ID = {bot.user.id}")
    print(discord.__version__)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=5, name="a massive gangbang")) # Displays 'Competing in a massive gangbang'
                                                    # type 0 = playing
                                                    # type 1 = streaming
                                                    # type 2 = listening to
                                                    # type 3 = watching
                                                    # type 4 = Custom (NOT SUPPORTED)
                                                    # type 5 = competeting in
    logs = bot.get_channel(791670764143247420)
    onstart = discord.Embed(
        title = f"{bot.user.name} is now online",
        color = random.randint(0, 0xffffff),
        timestamp = datetime.datetime.now(datetime.timezone.utc)
    )
    onstart.set_author(
        name = bot.user,
        icon_url = f"{embed_footer_icon}",
    )
    onstart.set_footer(text =f"{embed_footer}",
    icon_url=f"{embed_footer_icon}"
    )
    await logs.send(embed = onstart)




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
@bot.command(aliases=['hi'], description='Test if the bot is able to chat', help = "Says hello. What a nice bot.")
async def hello(ctx):
    await ctx.send('hello :)')





# Changeprefix command
@bot.command(aliases=['setprefix'], description="Usage: .prefix [NEW PREFIX]", help = "Changes the prefix. If empty, resets the prefix to default.")
async def prefix(ctx, prefixset = None):
    if (not ctx.author.guild_permissions.manage_channels):
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

@bot.command(aliases=['key','api', 'apikey'], description='Usage: .token', help="Shows the Token of this Bot")
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





# Simple clear message command
@bot.command(aliases = ['claer'], description="Usage: .clear [Amount of messages you want to delete]", help="Clears messages")
async def clear(ctx, amount=1):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send(f'{missing_perms}')
        return
    await ctx.channel.purge(limit=amount+1)





@bot.command(aliases=['av, avatar, avatar, avtar, avatr'], description="Usage: .avatar [USER @]", help="Displays a users avatar")
async def avatar(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar_url

    avatarEmbed = discord.Embed(title = f"{member.name}'s Avatar")
    avatarEmbed.set_image(url = memberAvatar)

    await ctx.send(embed = avatarEmbed)





@bot.command(name="commands", description="Usage: .commands", help="Lists every command available")
async def commands(ctx):
    commands = "```"
    for command in bot.commands:
        commands+=f"{command}\n"
    commands+="```"
    await ctx.send(commands)








@bot.command(pass_context=True, name = "restart", aliases = ["r"], description="Usage: .restart", help = "Restarts the bot.")
async def restart(ctx):
    logs = bot.get_channel(791670764143247420)
    restartembed = discord.Embed(
        title = f"{bot.user.name} is now restarting...",
        color = random.randint(0, 0xffffff),
        timestamp = datetime.datetime.now(datetime.timezone.utc)
    )
    restartembed.set_author(
        name = ctx.author.name,
        icon_url = ctx.author.avatar_url,
    )
    restartembed.set_footer(text =f"{embed_footer}",
    icon_url=f"{embed_footer_icon}"
    )
    if ctx.author.id != 399668151475765258:
        await ctx.send(f'{not_owner}')
        await ctx.message.add_reaction(emoji)
        return

    await logs.send(embed = restartembed)
    
    await ctx.message.add_reaction("✅")
    await bot.close()



bot.run(os.getenv("TOKEN"))