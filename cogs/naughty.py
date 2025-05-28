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



def setup(bot):
    bot.add_cog(NaughtyCommands(bot))
