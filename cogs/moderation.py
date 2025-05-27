import nextcord
from main import missing_perms
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @nextcord.slash_command(name="kick", description="Kicks a user")
    @commands.has_permissions(kick_members=True)
    @nextcord.slash_command(name="kick", description="Kicks a user")
    async def kick(
        self,
        i: Interaction,
        member: nextcord.Member = SlashOption(description="The member to kick"),
        reason: str = SlashOption(description="The reason for the kick", required=False),
    ):
        if member == i.user:
            await i.response.send_message(
                "You can't kick yourself, idiot. *Who hired this guy?*",
                ephemeral=True,
            )
            return

        # Permission already validated by decorator
        …
        await member.kick(reason=reason)
        await i.response.send_message(f"{member.mention} has been kicked.")


    @nextcord.slash_command(name="ban", description="Bans a user")
    async def ban(self, i: Interaction, member: nextcord.Member = SlashOption(description="The member to ban"), reason: str = SlashOption(description="The reason for the ban", required=False)):
        if member == i.user:
            await i.response.send_message("You can't ban yourself, idiot. *Who hired this guy?*")
            return
        if not i.user.guild_permissions.ban_members:
            await i.response.send_message(f'{missing_perms}', ephemeral=True)
            return
        await i.response.send_message(f"{member} has been banned.")
        await member.ban(reason=reason)



    @nextcord.slash_command(name="clear", description="Clears messages from the channel")
    async def clear(self, i: Interaction, amount: int = SlashOption(description="Amount of messages to be deleted")):
        if not i.user.guild_permissions.manage_messages:
            await i.response.send_message(f"{missing_perms}", ephemeral=True)
            return
        await i.channel.purge(limit=amount)
        await i.response.send_message(f"{amount} messages were successfully deleted", ephemeral=True)
        return
    

    
    @nextcord.slash_command(name="purge", description="Purges the whole channel")
    async def purge(self, i: Interaction):
        if not i.user.guild_permissions.manage_messages:
            await i.response.send_message(f"{missing_perms}", ephemeral=True)
            return
        await i.channel.purge()
        await i.response.send_message("The channel was purged", ephemeral=True)
        return



def setup(bot):
    bot.add_cog(ModerationCommands(bot))