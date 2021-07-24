import os
import discord
import random
import json
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents().all()
intents.members = True
emoji = '🤡'





# Prefix load from .json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]



# Getting Prefix
bot = commands.Bot(command_prefix= get_prefix, case_insensitive=True)



# Ready up message and activity status
@bot.event
async def on_ready():
    print('------')
    print(f"Logged in as {bot.user} ")
    print(f"User-ID = {bot.user.id}")
    print(discord.__version__)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=5, name="a massive gangbang")) # Displays 'Competing in a massive gangbang'





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
@bot.command(aliases=['hi'], description='Test if the bot is able to chat')
async def hello(ctx):
    await ctx.send('hello')





# Changeprefix command
@bot.command(aliases=['prefix'])
async def changeprefix(ctx, prefixset = None):
    if (not ctx.author.guild_permissions.manage_channels):
        await ctx.send('nooooo')
        return

    if prefixset is None:
        prefixset = '.'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'The bot prefix has been changed to ``{prefixset}``')






# Simple Embed message
@bot.command(description='Simple embed message')
async def em(ctx):
    embed=discord.Embed(title="Test embed message", description="testing my embed skills :)", color=random.randint(0, 0xffffff))
    embed.set_author(name=f"{ctx.message.author}", url="https://static.thenounproject.com/png/2420170-200.png", icon_url="https://static.thenounproject.com/png/2420170-200.png")
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.add_field(name="FELD", value="WERT", inline=False)
    embed.add_field(name="FELD 2", value="WERT 2", inline=False)
    embed.set_footer(text="made with 💛 by alex.")
    await ctx.send(embed=embed)





@bot.command(aliases=['key','api', 'apikey'], description='Shows the Token of this Bot')
async def Token(message):
    if message.author.id != 399668151475765258:
        await message.channel.send('You do not have permission to run this command')
    
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
@bot.command()
async def clear(ctx, amount=1):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the permission to run this command.\nAsk your Administrator for help.')
        return
    await ctx.channel.purge(limit=amount+1)





@bot.command()
async def avatar(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author

    memberAvatar = member.avatar_url

    avatarEmbed = discord.Embed(title = f"{member.name}'s Avatar")
    avatarEmbed.set_image(url = memberAvatar)

    await ctx.send(embed = avatarEmbed)













bot.run(os.getenv("TOKEN"))