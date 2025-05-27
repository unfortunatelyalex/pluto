import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


class NaughtyCommands(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the NaughtyCommands cog with a reference to the bot instance.
        """
        self.bot = bot

    @nextcord.slash_command(description="It's hentai, you know what hentai is.")
    async def hentai(self, i: Interaction, category: str = SlashOption(name="category", description="The hentai category", choices={"anal": "anal", "blowjob": "blowjob", "cum": "cum", "fuck": "fuck", "neko": "neko", "pussylick": "pussylick", "solo": "solo", "yaoi": "yaoi", "yuri": "yuri"})):
        """
        Fetches and sends a hentai GIF from a specified NSFW category.
        
        Checks if the command is used in an NSFW channel and retrieves a random hentai GIF from the selected category using the purrbot.site API. Sends an embed with the image if successful, or an ephemeral error message if not.
        
        Args:
            category: The hentai category to fetch a GIF from. Must be one of the predefined choices.
        """
        if not i.channel.is_nsfw():
            await i.response.send_message('You can\'t run this command in a non-nsfw channel', ephemeral=True)
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://purrbot.site/api/img/nsfw/{category}/gif') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = nextcord.Embed(title=f"NSFW - {category.title()}", color=0xff69b4)
                        embed.set_image(url=data['link'])
                        embed.set_footer(text="⚠️ NSFW Content")
                        await i.response.send_message(embed=embed)
                    else:
                        await i.response.send_message('Failed to fetch content from API', ephemeral=True)
        except Exception as e:
            await i.response.send_message(f'Error: {e}', ephemeral=True)

    @nextcord.slash_command(description="Posts a random image or video from the nsfw subreddit")
    async def nsfw(self, i: Interaction):
        """
        Posts a random NSFW image or video from the r/nsfw subreddit as an embed.
        
        Checks if the command is used in an NSFW channel before fetching a random post from Reddit. Sends an ephemeral error message if the channel is not NSFW or if content retrieval fails.
        """
        if not i.channel.is_nsfw():
            await i.response.send_message('You can\'t run this command in a non-nsfw channel', ephemeral=True)
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.reddit.com/r/nsfw/random.json') as r:
                    if r.status == 200:
                        data = await r.json()
                        post_data = data[0]['data']['children'][0]['data']
                        embed = nextcord.Embed(title=post_data['title'], color=0xff69b4)
                        embed.set_image(url=post_data['url'])
                        embed.set_footer(text=f"⚠️ NSFW Content | 👍 {post_data.get('ups', 0)}")
                        await i.response.send_message(embed=embed)
                    else:
                        await i.response.send_message('Failed to fetch content from Reddit', ephemeral=True)
        except Exception as e:
            await i.response.send_message(f'Error: {e}', ephemeral=True)



def setup(bot):
    """
    Registers the NaughtyCommands cog with the bot instance.
    
    Args:
        bot: The Discord bot instance to which the cog will be added.
    """
    bot.add_cog(NaughtyCommands(bot))
