import os
import psutil
import nextcord
import datetime
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import pytz


class SystemCommands(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the SystemCommands cog with a reference to the bot instance.
        """
        self.bot = bot

    @nextcord.slash_command(name="systeminfo", description="Get system load and memory usage")
    async def system_info(self, i: Interaction):
        """
        Responds with current system metrics including load averages, CPU usage, memory usage, disk usage, and uptime in an embedded message.
        
        Displays system statistics such as load averages (1, 5, and 15 minutes), CPU utilization, memory and disk usage (both as percentages and in gigabytes), and system uptime. Sends the information as an embed in response to the slash command. If an error occurs, sends an ephemeral error message with details.
        """
        try:
            load1, load5, load15 = os.getloadavg()

            memory_info = psutil.virtual_memory()

            cpu_usage = psutil.cpu_percent(interval=1)

            disk_usage = psutil.disk_usage('/')

            def bytes_to_gb(bytes_value):
                return bytes_value / (1024 ** 3)

            embed = nextcord.Embed(title="📊 System Information", color=0x00ff00)
            embed.add_field(
                name="🔄 System Load (1/5/15 min)",
                value=f"```{load1:.2f}\n{load5:.2f}\n{load15:.2f}```",
                inline=True
            )
            embed.add_field(
                name="🖥️ CPU Usage",
                value=f"```{cpu_usage}%```",
                inline=True
            )
            embed.add_field(
                name="💾 Memory Usage",
                value=f"```{memory_info.percent}%\n{bytes_to_gb(memory_info.used):.2f}GB / {bytes_to_gb(memory_info.total):.2f}GB```",
                inline=True
            )
            embed.add_field(
                name="💽 Disk Usage",
                value=f"```{disk_usage.percent}%\n{bytes_to_gb(disk_usage.used):.2f}GB / {bytes_to_gb(disk_usage.total):.2f}GB```",
                inline=True
            )
            
            try:
                uptime_seconds = psutil.boot_time()
                uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(uptime_seconds)
                embed.add_field(
                    name="⏰ System Uptime",
                    value=f"```{str(uptime).split('.')[0]}```",
                    inline=True
                )
            except:
                pass
            
            embed.set_footer(text=f"Requested by {i.user}")
            await i.response.send_message(embed=embed)
        except Exception as e:
            await i.response.send_message(f"Unexpected error: {str(e)}", ephemeral=True)

    @nextcord.slash_command(name="run", description="Run a command in the terminal")
    async def run_command(self, i: Interaction, command: str):
        """
        Executes a terminal command and returns the output, with safety checks and access control.
        
        Only a specific user can use this command. Blocks execution of potentially dangerous commands by checking for restricted keywords. If the command produces output, returns it in an embed; otherwise, sends a success message. Output is truncated if it exceeds 1900 characters. On error, sends an ephemeral error message.
        """
        if i.user.id != 399668151475765258:
            await i.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            dangerous_commands = ['rm', 'del', 'format', 'shutdown', 'reboot', 'sudo', 'chmod', 'chown']
            if any(dangerous in command.lower() for dangerous in dangerous_commands):
                await i.response.send_message("Dangerous command detected and blocked.", ephemeral=True)
                return
                
            result = os.popen(command).read()
            
            if len(result) > 1900:
                result = result[:1900] + "... (output truncated)"
            
            if result.strip():
                embed = nextcord.Embed(title="Command Output", color=0x00ff00)
                embed.add_field(name="Command", value=f"```bash\n{command}```", inline=False)
                embed.add_field(name="Output", value=f"```\n{result}```", inline=False)
                await i.response.send_message(embed=embed)
            else:
                await i.response.send_message("Command executed successfully (no output)", ephemeral=True)
        except Exception as e:
            await i.response.send_message(f"Unexpected error: {str(e)}", ephemeral=True)

    @nextcord.slash_command()
    async def test(self, i: Interaction):
        """
        Sends an embed displaying the interaction creation time in both UTC and Central European Time.
        
        The embed includes formatted timestamps for UTC and CET, along with the requesting user's information in the footer.
        """
        utc_time = i.created_at
        cet_time = utc_time.astimezone(pytz.timezone('Europe/Berlin'))
        
        embed = nextcord.Embed(title="🕐 Time Test", color=0x00ff00)
        embed.add_field(name="UTC Time", value=utc_time.strftime("%d-%m-%Y - %H:%M:%S"), inline=False)
        embed.add_field(name="CET Time", value=cet_time.strftime("%d-%m-%Y - %H:%M:%S"), inline=False)
        embed.set_footer(text=f"Requested by {i.user}")
        await i.response.send_message(embed=embed)


def setup(bot):
    """
    Registers the SystemCommands cog with the provided bot instance.
    """
    bot.add_cog(SystemCommands(bot))
