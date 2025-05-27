import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


class NaughtyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="It's hentai, you know what hentai is.")
    async def hentai(self, i: Interaction, category: str = SlashOption(name="category", description="The hentai category", choices={"anal": "anal", "blowjob": "blowjob", "cum": "cum", "fuck": "fuck", "neko": "neko", "pussylick": "pussylick", "solo": "solo", "yaoi": "yaoi", "yuri": "yuri"})):
        if not isinstance(i.channel, nextcord.TextChannel) or not i.channel.is_nsfw():
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
        if not i.channel.is_nsfw():
            await i.response.send_message('You can\'t run this command in a non-nsfw channel', ephemeral=True)
            return
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"User-Agent": "PlutoBot/1.0 (+https://github.com/unfortunatelyalex/pluto)"}  
                async with session.get('https://www.reddit.com/r/nsfw/random.json', headers=headers) as r:
                    
                    if r.status == 200:
                        data = await r.json()
                        post_data = data[0]['data']['children'][0]['data']
                        embed = nextcord.Embed(title=post_data['title'], color=0xff69b4)
                        if post_data['url'].endswith((".jpg", ".png", ".gif", ".jpeg", ".webp")):  
                            embed.set_image(url=post_data['url'])  
                        else:  
                            embed.add_field(name="Link", value=post_data['url'], inline=False)
                        embed.set_footer(text=f"⚠️ NSFW Content | 👍 {post_data.get('ups', 0)}")
                        await i.response.send_message(embed=embed)
                    else:
                        await i.response.send_message('Failed to fetch content from Reddit', ephemeral=True)
        except Exception as e:
            await i.response.send_message(f'Error: {e}', ephemeral=True)



def setup(bot):
    bot.add_cog(NaughtyCommands(bot))
