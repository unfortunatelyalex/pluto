import nextcord
from main import missing_perms
from nextcord.ext import commands
from nextcord import Interaction, SlashOption


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the ModerationCommands cog with the provided bot instance.
        """
        self.bot = bot



    @nextcord.slash_command(name="kick", description="Kicks a user")
    async def kick(self, i: Interaction, member: nextcord.Member = SlashOption(description="The member to kick"), reason: str = SlashOption(description="The reason for the kick", required=False)):
        """
        Kicks a specified member from the server via the /kick slash command.
        
        If the invoking user attempts to kick themselves, a humorous refusal message is sent. The command checks for the 'kick_members' permission before proceeding. Upon success, the targeted member is removed from the server and a confirmation message is sent.
        """
        if member == i.user:
            await i.response.send_message("You can't kick yourself, idiot. *Who hired this guy?*")
            return
        if (not i.user.guild_permissions.kick_members):
            await i.response.send_message(f'{missing_perms}')
            return
        await member.kick(reason=reason)
        await i.response.send_message(f"{member.mention} has been kicked.")


    @nextcord.slash_command(name="ban", description="Bans a user")
    async def ban(self, i: Interaction, member: nextcord.Member = SlashOption(description="The member to ban"), reason: str = SlashOption(description="The reason for the ban", required=False)):
        """
        Bans a specified member from the guild via a slash command.
        
        If the invoking user attempts to ban themselves, a humorous refusal message is sent. The command checks for the `ban_members` permission before proceeding. Upon success, the member is banned with an optional reason, and a confirmation message is sent.
        """
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
        """
        Deletes a specified number of messages from the current channel.
        
        Requires the invoking user to have the 'Manage Messages' permission. Sends an ephemeral confirmation message upon successful deletion.
        """
        if not i.user.guild_permissions.manage_messages:
            await i.response.send_message(f"{missing_perms}", ephemeral=True)
            return
        await i.channel.purge(limit=amount)
        await i.response.send_message(f"{amount} messages were successfully deleted", ephemeral=True)
        return
    

    
    @nextcord.slash_command(name="purge", description="Purges the whole channel")
    async def purge(self, i: Interaction):
        """
        Deletes all messages in the current channel if the user has message management permissions.
        
        Sends an ephemeral confirmation message upon completion or a permission error if the user lacks the required permissions.
        """
        if not i.user.guild_permissions.manage_messages:
            await i.response.send_message(f"{missing_perms}", ephemeral=True)
            return
        await i.channel.purge()
        await i.response.send_message("The channel was purged", ephemeral=True)
        return



def setup(bot):
    """
    Registers the ModerationCommands cog with the bot instance.
    
    Args:
        bot: The Nextcord bot instance to which the cog will be added.
    """
    bot.add_cog(ModerationCommands(bot))