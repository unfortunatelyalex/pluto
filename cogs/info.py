import os
import pathlib
import psutil
import nextcord
import datetime
from main import embed_footer
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


def _safe_user(obj):
    """Return the user/member object or None."""
    return obj if obj is not None else None


def _avatar_url(user) -> str | None:
    """Best-effort retrieval of a user's avatar (or default avatar) URL.

    Handles cases where user or its avatar attributes may be None to satisfy
    static analysis complaining about potential None attributes.
    """
    if user is None:
        return None
    avatar = getattr(user, "avatar", None)
    if avatar is not None:
        return getattr(avatar, "url", None)
    default_avatar = getattr(user, "default_avatar", None)
    if default_avatar is not None:
        return getattr(default_avatar, "url", None)
    return None


def _user_name(user) -> str:
    return getattr(user, "name", "Unknown")


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Information about a user")
    async def userinfo(
        self,
        i: Interaction,
        user: nextcord.Member = SlashOption(
            description="User to get info about", required=False
        ),
    ):
        if user is None:
            user = i.user
        fetch_user = await self.bot.fetch_user(user.id)
        embed = nextcord.Embed(title=f"Userinfo for {user.name}", color=0x202225)
        if user.avatar is not None:
            embed.set_thumbnail(url=f"{user.avatar.url}")
        else:
            embed.set_thumbnail(url=f"{user.default_avatar.url}")
        requester = _safe_user(getattr(i, "user", None))
        requester_name = _user_name(requester)
        requester_avatar = _avatar_url(requester)
        if requester_avatar:
            embed.set_author(name=requester_name, icon_url=requester_avatar)
        else:
            embed.set_author(name=requester_name)
        embed.add_field(
            name="General Info",
            value=f"> Joined Discord on `{user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> Joined Server on: `{user.joined_at.strftime('%d %b %Y %H:%M:%S') if hasattr(user, 'joined_at') and user.joined_at is not None else 'Not in server'}` \n> ID: `{user.id}` \n> Is bot?: `{user.bot}`",
            inline=False,
        )
        avatar_url = (
            user.avatar.url if user.avatar is not None else user.default_avatar.url
        )
        banner_value = (
            f"[View]({fetch_user.banner.url})"
            if fetch_user.banner is not None
            else "`NONE`"
        )
        embed.add_field(
            name="Profile",
            value=f"> Avatar: [View]({avatar_url})\n> Banner: {banner_value}",
            inline=False,
        )
        # Server Info section - only show if user is a server member
        if hasattr(user, "roles") and hasattr(user, "nick"):
            roles = " ".join(
                [role.mention for role in user.roles if role.name != "@everyone"]
            )
            embed.add_field(
                name="Server Info",
                value=f"> Nickname: `{user.nick}` \n> Roles (**{len(user.roles)}**): {roles} @everyone",
                inline=False,
            )
        footer_user = requester
        footer_icon_url = _avatar_url(footer_user)
        if footer_icon_url:
            embed.set_footer(
                text=f"Requested by {footer_user}", icon_url=footer_icon_url
            )
        else:
            embed.set_footer(text=f"Requested by {footer_user}")
        await i.response.send_message(embed=embed)

    @nextcord.slash_command(name="avatar", description="Displays a users avatar")
    async def avatar(
        self,
        i: Interaction,
        member: nextcord.Member = SlashOption(
            description="User to display the avatar of", required=False
        ),
    ):
        if member is None:
            member = i.user
        member_avatar = (
            member.avatar.url
            if member.avatar is not None
            else member.default_avatar.url
        )

        avatar_embed = nextcord.Embed(
            title=f"{member.name}'s Avatar",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        avatar_embed.set_image(url=member_avatar)
        bot_avatar = _avatar_url(getattr(self.bot, "user", None))
        if bot_avatar:
            avatar_embed.set_footer(text=f"{embed_footer}", icon_url=bot_avatar)
        else:
            avatar_embed.set_footer(text=f"{embed_footer}")

        await i.response.send_message(embed=avatar_embed)
        return

    @nextcord.slash_command(description="Information about the bot")
    async def about(self, i: Interaction):
        embed = nextcord.Embed(title=f"About {self.bot.user.name}", color=0x202225)
        embed.set_thumbnail(url=f"{self.bot.user.avatar.url}")
        embed.add_field(
            name="General Info",
            value=f"> Created on `{self.bot.user.created_at.strftime('%d %b %Y %H:%M:%S')}` \n> ID: `{self.bot.user.id}`",
            inline=False,
        )
        if self.bot.user.banner is not None:
            embed.add_field(
                name="Profile",
                value=f"> Avatar: [View]({self.bot.user.avatar.url})\n> Banner: [View]({self.bot.user.banner.url})",
                inline=False,
            )
        else:
            embed.add_field(
                name="Profile",
                value=f"> Avatar: [View]({self.bot.user.avatar.url})\n> Banner: `NONE`",
                inline=False,
            )
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / float(2**20)
        embed.add_field(
            name="Host",
            value=f"> CPU usage: {psutil.cpu_percent(interval=1)}% \n> RAM usage: {round(mem)}MB",
            inline=False,
        )
        # derive project root (…/pluto) dynamically
        BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
        cogs_dir = BASE_DIR / "cogs"
        line_count = 0

        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(cogs_dir, filename)
                with open(filepath, "r") as file:
                    line_count += len(file.readlines())

        main_file = BASE_DIR / "main.py"
        with open(main_file, "r") as file:
            line_count += len(file.readlines())
        embed.add_field(
            name="About Me",
            value=f"> Guild count: `{len(self.bot.guilds)}` \n> Line count: `{line_count}` \n> Made by: `alexdot`",
            inline=False,
        )
        requester = _safe_user(getattr(i, "user", None))
        requester_name = _user_name(requester)
        requester_avatar = _avatar_url(requester)
        if requester_avatar:
            embed.set_author(name=requester_name, icon_url=requester_avatar)
        else:
            embed.set_author(name=requester_name)
        await i.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
