import os
import discord
from discord import message
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
import asyncio


load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():
    print('------')
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def hello(ctx):
    await ctx.send('hello')



client.run(os.getenv("TOKEN"))
