import json
import random
import traceback
import aiohttp
import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the FunCommands cog with a reference to the bot instance.
        """
        self.bot = bot

    @nextcord.slash_command(name="roastme", description="Yo Mama!")
    async def roastme(self, i: Interaction):
        """
        Sends a randomly selected roast from a local JSON file in response to a slash command.
        
        Reads roast categories and phrases from 'roastme.json', selects a random roast, and sends it as a message. If an error occurs, the error message is sent instead.
        """
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
        """
        Sends a random dog image in response to the user.
        
        Fetches a random dog image URL from the Dog CEO API and sends it as a message. If an error occurs during the request, the error message is sent instead.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                    data = await r.json()
                    await i.response.send_message(data['message'])
        except Exception as e:
            await i.response.send_message(f'{e}')



    @nextcord.slash_command(name="cat", description="Posts a random cat picture from the cat api")
    async def cat(self, i: Interaction):
        """
        Sends a random cat image in response to the slash command.
        
        Fetches a random cat image URL from the Random Cat API and sends it as a message. If an error occurs during the request, the error message is sent instead.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://aws.random.cat/meow') as r:
                    data = await r.json()
                    await i.response.send_message(data['file'])
        except Exception as e:
            await i.response.send_message(f'{e}')



    @nextcord.slash_command(name="meme", description="Posts a random meme from the dankmemes subreddit")
    async def meme(self, i: Interaction):
        """
        Sends a random meme image from the r/memes subreddit.
        
        Fetches a random meme by querying Reddit's random endpoint and sends the meme's image URL as a response. If an error occurs during the request or data processing, the error message is sent instead.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.reddit.com/r/memes/random.json') as r:
                    data = await r.json()
                    await i.response.send_message(data[0]['data']['children'][0]['data']['url'])
        except Exception as e:
            await i.response.send_message(f'{e}')

    

    @nextcord.slash_command(name="joke", description="Posts a random joke from the joke api")
    async def joke(self, i: Interaction):
        """
        Sends a random joke to the user by fetching it from the Official Joke API.
        
        The joke consists of a setup and punchline, delivered as a single message.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/jokes/random') as r:
                data = await r.json()
                await i.response.send_message(f'{data["setup"]}\n{data["punchline"]}')
        
    @joke.error
    async def joke_error(self, i: Interaction, error):
        """
        Handles errors for the joke command by notifying the user if the joke API is unavailable and logging detailed error information to the console.
        """
        if isinstance(error, commands.CommandInvokeError):
            await i.send("The joke api is down. Please try again later.")
            
        error_message = str(error.original) if hasattr(error, 'original') else str(error)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        traceback_str = "".join(tb).strip()

        print(f"Error in joke command: {error_message}\n{traceback_str}")


def setup(bot):
    """
    Registers the FunCommands cog with the bot.
    
    This function should be called to add the FunCommands cog when the module is loaded.
    """
    bot.add_cog(FunCommands(bot))