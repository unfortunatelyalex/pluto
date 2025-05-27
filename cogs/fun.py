import json
import random
import traceback
import aiohttp
import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="roastme", description="Yo Mama!")
    async def roastme(self, i: Interaction):
        try:
            with open('roastme.json', encoding="utf8") as f:
                data = json.load(f)
            category = random.choice(list(data.keys()))
            roast = random.choice(data[category])
            await i.response.send_message(f'{roast}')
        except Exception as e:
            await i.response.send_message(f'{e}')



    @nextcord.slash_command(name="dog", description="Posts a random dog picture from the dog api")
    async def dog(self, i: Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                    data = await r.json()
                    await i.response.send_message(data['message'])
        except Exception as e:
            await i.response.send_message(f'{e}')



    @nextcord.slash_command(name="cat", description="Posts a random cat picture from the cat api")
    async def cat(self, i: Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://aws.random.cat/meow') as r:
                    data = await r.json()
                    await i.response.send_message(data['file'])
        except Exception as e:
            await i.response.send_message(f'{e}')



    @nextcord.slash_command(name="meme", description="Posts a random meme from the dankmemes subreddit")
    async def meme(self, i: Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.reddit.com/r/memes/random.json') as r:
                    data = await r.json()
                    await i.response.send_message(data[0]['data']['children'][0]['data']['url'])
        except Exception as e:
            await i.response.send_message(f'{e}')

    

    @nextcord.slash_command(name="joke", description="Posts a random joke from the joke api")
    async def joke(self, i: Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/jokes/random') as r:
                data = await r.json()
                await i.response.send_message(f'{data["setup"]}\n{data["punchline"]}')
        
    @joke.error
    async def joke_error(self, i: Interaction, error):
        if isinstance(error, commands.CommandInvokeError):
            await i.response.send_message("The joke API is down. Please try again later.", ephemeral=True)
            
        error_message = str(error.original) if hasattr(error, 'original') else str(error)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        traceback_str = "".join(tb).strip()

        print(f"Error in joke command: {error_message}\n{traceback_str}")


def setup(bot):
    bot.add_cog(FunCommands(bot))