import os
import psutil
import nextcord
import datetime
from main import embed_footer
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @nextcord.slash_command(description="Information about a user")
        embed.set_footer(
            text=f"Requested by {i.user}",
            icon_url=i.user.avatar.url
        )
-        await i.send(embed=embed)
+        await i.response.send_message(embed=embed)



    @nextcord.slash_command(name="avatar", description="Displays a users avatar")
    async def avatar(self, i: Interaction, member: nextcord.Member = SlashOption(description="User to display the avatar of", required=False)):
        if member is None:
            member = i.user
        member_avatar = member.avatar.url

        avatar_embed = nextcord.Embed(
            title=f"{member.name}'s Avatar", timestamp=datetime.datetime.now(datetime.timezone.utc))
        avatar_embed.set_image(url=member_avatar)
        avatar_embed.set_footer(
            text=f"{embed_footer}", icon_url=f"{self.bot.user.avatar.url}")

        await i.response.send_message(embed=avatar_embed)
        return
    


    @nextcord.slash_command(description="Information about the bot")
    async def about(self, i: Interaction):
        embed = nextcord.Embed(title=f'About {self.bot.user.name}', color=0x202225)
        embed.set_thumbnail(
            url=f"{self.bot.user.avatar.url}"
        )
        embed.add_field(
            name="General Info",
            value=f"> Created on `{self.bot.user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{self.bot.user.id}`",
            inline=False
        )
        if self.bot.user.banner is not None:
            embed.add_field(
                name="Profile",
                value=f"> Avatar: [View]({self.bot.user.avatar.url})\n> Banner: [View]({self.bot.user.banner.url})",
                inline=False
            )
        else:
            embed.add_field(
                name="Profile",
                value=f"> Avatar: [View]({self.bot.user.avatar.url})\n> Banner: `NONE`",
                inline=False
            )
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / float(2 ** 20)
        embed.add_field(
            name="Host",
            value=f"> CPU usage: {psutil.cpu_percent(interval=1)}% \n> RAM usage: {round(mem)}MB",
            inline=False
        )
        # derive project root (…/pluto) dynamically
        BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
        cogs_dir = BASE_DIR / "cogs"
        line_count = 0

        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):        
                filepath = os.path.join(cogs_dir, filename)
                with open(filepath, 'r') as file:
                    line_count += len(file.readlines())

        main_file = BASE_DIR / "main.py"
        with open(main_file, 'r') as file:
            line_count += len(file.readlines())
        embed.add_field(
            name="About Me",
            value=f"> Guild count: `{len(self.bot.guilds)}` \n> Line count: `{line_count}` \n> Made by: `alexdot`",
            inline=False
        )
        if i.user.avatar is not None:
            embed.set_author(
                name=f"{i.user.name}",
                icon_url=f"{i.user.avatar.url}"
            )
        else:
            embed.set_author(
                name=f"{i.user.name}",
                icon_url=f"{i.user.default_avatar.url}"
            )
        await i.send(embed=embed)



def setup(bot):
    bot.add_cog(Info(bot))
