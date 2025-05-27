import os
import psutil
import nextcord
import datetime
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import pytz


class SystemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="systeminfo", description="Get system load and memory usage")
    async def system_info(self, i: Interaction):
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
                    value=f"
            embed.set_footer(text=f"Requested by {i.user}")
            await i.response.send_message(embed=embed)
        except Exception as e:
            await i.response.send_message(f"Unexpected error: {str(e)}", ephemeral=True)

# At the top of the file, replace your import of os (and bring in the new modules):
-import os, shlex, asyncio, subprocess
+import asyncio, shlex, subprocess

    @nextcord.slash_command(name="run", description="Run a command in the terminal")
    async def run_command(self, i: Interaction, command: str):
        if i.user.id != 399668151475765258:
            await i.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            dangerous_commands = ['rm', 'del', 'format', 'shutdown', 'reboot', 'sudo', 'chmod', 'chown']
            if any(dangerous in command.lower() for dangerous in dangerous_commands):
                await i.response.send_message("Dangerous command detected and blocked.", ephemeral=True)
                return

-            result = os.popen(command).read()
+            # Run in executor to avoid blocking and bypass a shell
+            loop = asyncio.get_running_loop()
+            proc = await loop.run_in_executor(
+                None,
+                lambda: subprocess.run(
+                    shlex.split(command),
+                    capture_output=True,
+                    text=True,
+                    timeout=10,
+                ),
+            )
+            result = proc.stdout or proc.stderr

            if len(result) > 1900:
                result = result[:1900] + "... (output truncated)"

            if result.strip():
                embed = nextcord.Embed(title="Command Output", color=0x00ff00)
                embed.add_field(name="Command", value=f"

    @nextcord.slash_command()
    async def test(self, i: Interaction):
        utc_time = i.created_at
        cet_time = utc_time.astimezone(pytz.timezone('Europe/Berlin'))
        
        embed = nextcord.Embed(title="🕐 Time Test", color=0x00ff00)
        embed.add_field(name="UTC Time", value=utc_time.strftime("%d-%m-%Y - %H:%M:%S"), inline=False)
        embed.add_field(name="CET Time", value=cet_time.strftime("%d-%m-%Y - %H:%M:%S"), inline=False)
        embed.set_footer(text=f"Requested by {i.user}")
        await i.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(SystemCommands(bot))
