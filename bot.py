import os
import discord
import random
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.members = True

emoji = '🤡'



# Prefix

bot = commands.Bot(command_prefix='+')



# Ready up message and activity status

@bot.event
async def on_ready():
    print('------')
    print(f"Logged in as {bot.user} ")
    print(f"User-ID = {bot.user.id}")
    print(discord.__version__)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=5, name="a massive gangbang")) # Displays 'Competing in a massive gangbang'



# Test command

@bot.command()
async def hello(ctx):
    await ctx.send('hello')



@bot.command()
async def em(ctx):
    embed=discord.Embed(title="Test embed message", description="testing my embed skills :)", color=random.randint(0, 0xffffff))
    embed.set_author(name=f"{ctx.message.author}", url="https://static.thenounproject.com/png/2420170-200.png", icon_url="https://static.thenounproject.com/png/2420170-200.png")
    embed.set_thumbnail(url="https://static.thenounproject.com/png/2420170-200.png")
    embed.add_field(name="FELD", value="WERT", inline=False)
    embed.add_field(name="FELD 2", value="WERT 2", inline=False)
    embed.set_footer(text="made with 💛 by alex.")
    await ctx.send(embed=embed)



# REACTION TO EVERY MESSAGE FROM GIVEN USERID

@bot.event
async def on_message(message):
    if message.author.id == 406456604825747466:
        await message.add_reaction(emoji)

    await bot.process_commands(message)


# Simple clear message command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=4):
    await ctx.channel.purge(limit=amount+1) 













bot.run(os.getenv("TOKEN"))