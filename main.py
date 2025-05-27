import os
import json
import random
import datetime
import nextcord
from   dotenv       import load_dotenv
from   nextcord.ui  import Button, View
from   nextcord.ext import commands
from   nextcord     import Interaction, ButtonStyle


class Database:
    def __init__(self, filename='session_data.json'):
        self.filename = filename

    def save(self, listening_channel_id, session_name):
        session_data = {"listening_channel_id": listening_channel_id, "session_name": session_name}
        with open(self.filename, 'w') as f:
            json.dump(session_data, f)

    def load(self):
        with open(self.filename, 'r') as f:
            session_data = json.load(f)
        return session_data["listening_channel_id"], session_data["session_name"]


load_dotenv()


intents = nextcord.Intents.default()
intents.message_content = True
embed_footer = 'made with 💛 by alexdot'
embed_footer_icon = "https://cdn.discordapp.com/avatars/791670415779954698/2a9cdb3b39a17dc0682572b806bd3ceb.webp?size=1024"
missing_perms = "Unable to run this command.\nReason: (MissingPermissions)\nIf you believe this could be a mistake, please contact your administrator."
not_owner = "You don't own this bot to run this command\nReason: (NotOwner)\nIf you believe this could be a mistake, please contact your administrator."
perminv = os.getenv("botinv")
dm_logs = "984869415684284536"


bot = commands.Bot(owner_id="399668151475765258", intents=intents, command_prefix=",")
bot.remove_command('help')



# Ready up message and activity status
@bot.event
async def on_ready():
    print('--------------------------------')
    print(f"     Logged in as {bot.user} ")
    print(f" User-ID = {bot.user.id}")
    print(f"      Version = {nextcord.__version__}")
    print('--------------------------------')
    custom = nextcord.CustomActivity(name="Nothing lasts forever but I wish we did", emoji="<:point:916333529623846922>")
    await bot.change_presence(activity=custom, status=nextcord.Status.online)
    # playing      = type 0, name="NAME"
    # streaming    = type 1, name="NAME", url=YOUTUBE/TWITCH
    # listening to = type 2, name="NAME"
    # watching     = type 3, name="NAME"
    # CUSTOM       = type 4 (NOT SUPPORTED)
    # COMPETING IN = type 5, name="NAME"
    logs = bot.get_channel(791670764143247420)
    onstart = nextcord.Embed(
        title=f"{bot.user.name} is now online",
        description="<@399668151475765258> read this <:point:916333529623846922>",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    onstart.set_author(
        name=bot.user.name,
        icon_url=f"{embed_footer_icon}"
    )
    onstart.set_footer(text=f"{embed_footer}", icon_url=f"{embed_footer_icon}")
    await logs.send(embed=onstart)





# Deleted message log
@bot.event
async def on_message_delete(message):
    if message.guild.id == 791670762859266078:
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(
            title='Message Deleted', description=f'{message.author.mention} deleted the message: {message.content}\n In the channel {message.channel.mention}', color=0x00ff00)
        embed.set_footer(text=f'{message.author}',
                         icon_url=message.author.display_avatar)
        await channel.send(embed=embed)

# Edited message log
@bot.event
async def on_message_edit(before, after):
    if before.guild.id == 791670762859266078:
        if before.author.bot:
            return
        channel = bot.get_channel(956820109823987712)
        embed = nextcord.Embed(
            title='Message Edited', description=f'{before.author.mention} edited the message: ```{before.content}``` to\n ```{after.content}```', color=0x00ff00)
        embed.set_footer(text=f'{before.author}',
                         icon_url=before.author.display_avatar)
        await channel.send(embed=embed)


# Dms from user to a channel
@bot.event
async def on_message(message: nextcord.Message):
    channel = bot.get_channel(984869415684284536)
    attachment = nextcord.Attachment
    if message.guild is None and not message.author.bot and isinstance(message.attachments, list):
        for attachment in message.attachments:
            if attachment.filename.endswith((".png", ".jpg", ".gif", ".jpeg", ".mp4", ".webm", ".mp3", ".wav", ".mov")):
                await channel.send(f"<@!399668151475765258>\n{message.author.mention} sent a picture: {attachment.url}\nMessage content: `{message.content}`")
                return
    if message.guild is None and not message.author.bot:
        await channel.send(f"<@!399668151475765258>\nNew message from {message.author.mention}:\nMessage content: `{message.content}`")
        await bot.process_commands(message)
        return
    if message.guild is not None:
        await bot.process_commands(message)
        return


if __name__ == "__main__":
    print("Starting to load extensions...")

    loaded_extensions = set()

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename not in loaded_extensions:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename}")
            loaded_extensions.add(filename)

    print("Finished loading extensions.")
    bot.run(os.getenv("TOKEN"))
