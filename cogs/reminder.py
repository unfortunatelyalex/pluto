import aiohttp
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, TextChannel, Embed, Color
from nextcord.ui import View, Button, Modal, TextInput
import datetime
import json
import os
import re
import uuid
from logging.handlers import RotatingFileHandler
import logging
import zoneinfo
from main import embed_footer
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

# Configure logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

# Logging setup: separate files for info, debug, and error
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

info_handler = RotatingFileHandler(os.path.join(LOG_DIR, "reminder_info.log"), maxBytes=5000000, backupCount=3, encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(LOG_FORMAT))

debug_handler = RotatingFileHandler(os.path.join(LOG_DIR, "reminder_debug.log"), maxBytes=5000000, backupCount=3, encoding="utf-8")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter(LOG_FORMAT))

def error_filter(record):
    """
    Filters log records, allowing only those with level ERROR or higher.
    """
    return record.levelno >= logging.ERROR

error_handler = RotatingFileHandler(os.path.join(LOG_DIR, "reminder_error.log"), maxBytes=5000000, backupCount=3, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(error_filter)
error_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Remove default handlers and add our custom ones
logger = logging.getLogger(__name__)
for h in list(logger.handlers):
    logger.removeHandler(h)
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)

CACHE_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminders_cache.json")
USER_TZ_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_timezones.json")

class TimezoneModal(Modal):
    def __init__(self, user_id, callback):
        """
        Initializes the TimezoneModal for user timezone input.
        
        Creates a modal dialog prompting the user to enter their timezone, storing the user ID and a callback function to handle the submitted value.
        """
        super().__init__("Set Your Timezone")
        self.user_id = user_id
        self.callback_func = callback
        self.tz_input = TextInput(
            label="Enter your timezone (e.g., Europe/Berlin)",
            placeholder="Europe/Berlin",
            required=True,
            min_length=3,
            max_length=64
        )
        self.add_item(self.tz_input)

    async def callback(self, interaction: Interaction):
        """
        Validates the user's timezone input from the modal and handles the result.
        
        If the input is a valid timezone, invokes the provided callback with the interaction and timezone. If invalid, sends an ephemeral error embed with example timezones and a retry button. Handles unexpected errors by logging and notifying the user.
        """
        tz = self.tz_input.value.strip()
        try:
            # Validate the timezone
            zoneinfo.ZoneInfo(tz)
            await self.callback_func(interaction, tz)
        except zoneinfo.ZoneInfoNotFoundError:
            # Create retry view with button
            class TryAgainView(View):
                def __init__(self, user_id, callback_func):
                    """
                    Initializes the view with a "Try Again" button for timezone input.
                    
                    Args:
                        user_id: The ID of the user who should interact with the button.
                        callback_func: The function to call when the user clicks the button.
                    """
                    super().__init__(timeout=120)
                    self.add_item(TryAgainButton(user_id, callback_func))
                    
            class TryAgainButton(Button):
                def __init__(self, user_id, callback_func):
                    """
                    Initializes the button for retrying timezone input with user and callback context.
                    
                    Args:
                        user_id: The ID of the user who initiated the timezone input.
                        callback_func: The function to call when the button is pressed.
                    """
                    super().__init__(label="Try Again", style=nextcord.ButtonStyle.danger)
                    self.user_id = user_id
                    self.callback_func = callback_func
                    
                async def callback(self, btn_interaction: Interaction):
                    """
                    Handles the button interaction for setting a user's timezone.
                    
                    If the interacting user matches the intended user, opens the timezone input modal; otherwise, sends an ephemeral error message.
                    """
                    if btn_interaction.user.id != self.user_id:
                        await btn_interaction.response.send_message("You can't set the timezone for another user!", ephemeral=True)
                        return
                    await btn_interaction.response.send_modal(TimezoneModal(self.user_id, self.callback_func))
            
            error_embed = nextcord.Embed(
                title="❌ Invalid Timezone",
                description=f"'{tz}' is not a valid timezone.",
                color=0xff0000
            )
            error_embed.add_field(
                name="💡 Examples",
                value="• `Europe/Berlin`\n• `America/New_York`\n• `Asia/Tokyo`\n• `UTC`",
                inline=False
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True,
                view=TryAgainView(self.user_id, self.callback_func)
            )
        except Exception as e:
            # Log and show a generic error for unexpected issues
            logger.error(f"Unexpected error validating timezone '{tz}': {e}", exc_info=True)
            error_embed = nextcord.Embed(
                title="❌ Error",
                description="An unexpected error occurred. Please try again later.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

class TimezoneView(View):
    def __init__(self, user_id, callback):
        """
        Initializes the TimezoneView with a button for setting the user's timezone.
        
        Args:
            user_id: The Discord user ID for whom the timezone is being set.
            callback: Function to call when the timezone is successfully set.
        """
        super().__init__(timeout=120)
        self.user_id = user_id
        self.callback_func = callback
        self.add_item(TimezoneButton(user_id, callback))

class TimezoneButton(Button):
    def __init__(self, user_id, callback):
        """
        Initializes a button for users to set their timezone.
        
        Args:
            user_id: The Discord user ID authorized to interact with this button.
            callback: Function to call when the timezone modal is submitted.
        """
        super().__init__(label="Set Timezone", style=nextcord.ButtonStyle.primary)
        self.user_id = user_id
        self.callback_func = callback

    async def callback(self, interaction: Interaction):
        """
        Handles the button click event to initiate timezone setting for the intended user.
        
        If the interacting user matches the expected user ID, opens the timezone input modal; otherwise, sends an ephemeral error message.
        """
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't set the timezone for another user!", ephemeral=True)
            return
        await interaction.response.send_modal(TimezoneModal(self.user_id, self.callback_func))

class ReminderCommand(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the ReminderCommand cog, loading reminders from persistent storage and preparing internal state.
        
        Args:
        	bot: The Discord bot instance to which this cog is attached.
        """
        self.bot = bot
        self.reminders = []
        self._pending_reminders = {}  # user_id: (interaction, args_dict)
        logger.info("ReminderCommand Cog __init__ called.")
        self._load_reminders()
        try:
            logger.info("check_reminders_loop start call prepared in __init__.")
        except Exception as e:
            logger.error(f"Error preparing check_reminders_loop in __init__: {e}", exc_info=True)

    def cog_unload(self):
        """
        Handles cleanup when the cog is unloaded by canceling the reminder checking loop and saving reminders to persistent storage.
        """
        try:
            self.check_reminders_loop.cancel()
            logger.info("check_reminders_loop cancelled in cog_unload.")
        except Exception as e:
            logger.error(f"Failed to cancel check_reminders_loop in cog_unload: {e}", exc_info=True)
        self._save_reminders()

    def _load_user_timezones(self):
        """
        Loads user timezone mappings from persistent storage.
        
        Returns:
            A dictionary mapping user IDs to timezone strings. Returns an empty dictionary if the file does not exist or cannot be read.
        """
        if os.path.exists(USER_TZ_PATH):
            try:
                with open(USER_TZ_PATH, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load user timezones: {e}")
        return {}

    def _save_user_timezones(self, tz_dict):
        """
        Saves the user timezone mappings to a JSON file.
        
        Args:
            tz_dict: A dictionary mapping user IDs to timezone strings.
        """
        try:
            with open(USER_TZ_PATH, 'w') as f:
                json.dump(tz_dict, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save user timezones: {e}")

    def _get_user_timezone(self, user_id):
        """
        Retrieves the stored timezone string for a given user ID.
        
        Args:
            user_id: The Discord user ID whose timezone is being requested.
        
        Returns:
            The timezone string if set for the user, otherwise None.
        """
        tz_dict = self._load_user_timezones()
        return tz_dict.get(str(user_id))

    def _set_user_timezone(self, user_id, tz):
        """
        Sets the timezone for a user and saves the updated mapping persistently.
        
        Args:
            user_id: The Discord user ID whose timezone is being set.
            tz: The IANA timezone string to associate with the user.
        """
        tz_dict = self._load_user_timezones()
        tz_dict[str(user_id)] = tz
        self._save_user_timezones(tz_dict)

    async def _ask_timezone(self, interaction, on_timezone_set, pending_args=None):
        """
        Prompts the user to set their timezone before proceeding with a reminder.
        
        If the user has not set a timezone, sends an ephemeral embed with instructions and a button to initiate timezone selection. Stores any pending reminder arguments for processing after the timezone is set.
        """
        try:
            tz_link = "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            
            embed = nextcord.Embed(
                title="🌍 Timezone Required",
                description=f"Hi {interaction.user.mention}! Please set your timezone before using reminders.",
                color=0x00a2e8
            )
            embed.add_field(
                name="📋 Instructions",
                value="Click the button below to set your timezone.\nExample timezones: `Europe/Berlin`, `America/New_York`, `Asia/Tokyo`",
                inline=False
            )
            embed.add_field(
                name="🔗 Timezone List",
                value=f"[Click here for full timezone list]({tz_link})",
                inline=False
            )
            embed.set_footer(
                text=f"{embed_footer}",
                icon_url=self.bot.user.display_avatar.url if self.bot.user else None
            )
            
            view = TimezoneView(interaction.user.id, on_timezone_set)
            if pending_args:
                self._pending_reminders[interaction.user.id] = (interaction, pending_args)
            await interaction.send(embed=embed, view=view, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error in _ask_timezone: {e}", exc_info=True)
            await interaction.send("An error occurred while setting up timezone selection.", ephemeral=True)

    async def _on_timezone_set(self, interaction, tz):
        """
        Handles the user's timezone selection, confirms the update, and processes any pending reminder.
        
        If the user had a reminder pending due to missing timezone information, this method processes it after setting the timezone. Sends a confirmation or error embed to the user.
        """
        try:
            self._set_user_timezone(interaction.user.id, tz)
            
            embed = nextcord.Embed(
                title="✅ Timezone Set",
                description=f"Timezone set to **{tz}**. Now processing your reminder...",
                color=0x00ff00
            )
            embed.set_footer(
                text=f"{embed_footer}",
                icon_url=self.bot.user.display_avatar.url if self.bot.user else None
            )
            
            await interaction.send(embed=embed, ephemeral=True)
            
            # Check if we have a pending reminder for this user
            pending = self._pending_reminders.pop(interaction.user.id, None)
            if pending:
                _, args = pending
                # Call the remind logic with the original arguments
                await self._process_remind(**args)
                
        except Exception as e:
            logger.error(f"Error in _on_timezone_set: {e}", exc_info=True)
            error_embed = nextcord.Embed(
                title="❌ Error",
                description="An error occurred while setting your timezone.",
                color=0xff0000
            )
            await interaction.send(embed=error_embed, ephemeral=True)

    async def _process_remind(self, i, message, time, title, topic, channel):
        """
        Processes a reminder request by scheduling a Discord reminder and sending a notification via ntfy.
        
        Attempts to parse the provided time string using the user's timezone, schedules a Discord reminder if the time is valid and in the future, and sends a notification to the specified ntfy topic. Responds to the user with an embed summarizing the status of both the Discord reminder and the ntfy notification. Handles invalid channels, time parsing errors, and network or unexpected exceptions with appropriate user feedback.
        """
        user_tz = self._get_user_timezone(i.user.id)
        logger.info(f"Remind command invoked by {i.user} (ID: {i.user.id}) with time='{time}', message='{message}', title='{title}', topic='{topic}', channel='{channel}'")
        
        try:
            target_discord_channel = channel if channel else i.channel
            if not isinstance(target_discord_channel, TextChannel):
                logger.warning(f"Invalid channel for reminder: {target_discord_channel} (type: {type(target_discord_channel)}). User: {i.user}")
                error_embed = nextcord.Embed(
                    title="❌ Invalid Channel",
                    description="Invalid channel selected or current channel is not a text channel. Cannot set Discord reminder.",
                    color=0xff0000
                )
                await i.send(embed=error_embed, ephemeral=True)
                return

            ntfy_topic_actual = topic if topic else "reminders"
            ntfy_title_actual = title if title else "Reminder!"

            headers_ntfy = {
                "Authorization": f"Basic {os.getenv("NTFY_AUTH_TOKEN")}",
                "Title": ntfy_title_actual,
            }
            if time:
                headers_ntfy["In"] = time 

            ntfy_url = f"https://ntfy.alexdot.me/{ntfy_topic_actual}"
            ntfy_success = False
            ntfy_error_message = ""

            try:
                async with aiohttp.ClientSession() as session:
                    logger.debug(f"Sending NTFY request to {ntfy_url} with headers {headers_ntfy} and data '{message}'")
                    async with session.post(ntfy_url, headers=headers_ntfy, data=message.encode('utf-8')) as response:
                        response_text = await response.text()
                        if response.status == 200:
                            ntfy_success = True
                            logger.info(f"Ntfy reminder sent successfully for user {i.user.id}. Response: {response_text[:200]}")
                        else:
                            ntfy_error_message = f"Ntfy failed: {response.status} - {response_text}"
                            logger.error(f"Ntfy error for user {i.user.id}: {ntfy_error_message}")
            except aiohttp.ClientError as e:
                ntfy_error_message = f"Ntfy request failed: {e}"
                logger.error(f"Ntfy ClientError for user {i.user.id}: {e}", exc_info=True)
            
            due_datetime_discord = self._parse_time_to_datetime(time, user_tz)
            logger.info(f"Parsed time '{time}' for Discord. Resulting due_datetime_discord: {due_datetime_discord.isoformat() if due_datetime_discord else 'None'} (for user {i.user.id})")
            
            discord_reminder_scheduled_msg = ""
            success_color = 0x00ff00
            warning_color = 0xffa500

            if due_datetime_discord:
                current_utc_time = datetime.datetime.now(datetime.timezone.utc)
                logger.debug(f"Comparing due_datetime_discord ({due_datetime_discord.isoformat()}) with current_utc_time ({current_utc_time.isoformat()})")
                if due_datetime_discord > current_utc_time:
                    reminder_id = str(uuid.uuid4())
                    reminder_data = {
                        "id": reminder_id,
                        "user_id": i.user.id,
                        "channel_id": target_discord_channel.id,
                        "guild_id": i.guild.id if i.guild else None,
                        "title": ntfy_title_actual,
                        "message": message,
                        "due_timestamp": due_datetime_discord.timestamp(),
                        "original_time_str": time,
                    }
                    self.reminders.append(reminder_data)
                    self._save_reminders()
                    discord_reminder_scheduled_msg = f"Discord reminder scheduled for {nextcord.utils.format_dt(due_datetime_discord, 'F')} in {target_discord_channel.mention}."
                    logger.info(f"Scheduled Discord reminder ID {reminder_id} for user {i.user.id} at {due_datetime_discord.isoformat()}.")
                else:
                    discord_reminder_scheduled_msg = "Could not schedule Discord reminder: The calculated time is in the past."
                    logger.warning(f"Discord reminder time ({due_datetime_discord.isoformat()}) is in the past compared to current time ({current_utc_time.isoformat()}) for user {i.user.id}. Original time string: '{time}'")
                    success_color = warning_color
            else:
                discord_reminder_scheduled_msg = f"Could not parse '{time}' for a Discord reminder. Please use formats like '10m', '2h', '1d', 'tomorrow', 'tomorrow 3pm', '16:30'."
                logger.warning(f"Failed to parse time '{time}' for Discord reminder for user {i.user.id}. _parse_time_to_datetime returned None.")
                success_color = warning_color

            # Create an embed response
            embed = nextcord.Embed(
                title="⏰ Reminder Status",
                color=success_color if ntfy_success or due_datetime_discord else 0xff0000
            )

            if ntfy_success:
                embed.add_field(
                    name="📱 Ntfy Notification", 
                    value="✅ Sent/scheduled successfully", 
                    inline=False
                )
            else:
                brief_ntfy_error = ntfy_error_message.splitlines()[0] if ntfy_error_message else "Unknown error"
                embed.add_field(
                    name="📱 Ntfy Notification", 
                    value=f"❌ Failed: {brief_ntfy_error}", 
                    inline=False
                )
            
            if discord_reminder_scheduled_msg:
                status_icon = "✅" if "scheduled for" in discord_reminder_scheduled_msg else "⚠️"
                embed.add_field(
                    name="💬 Discord Reminder", 
                    value=f"{status_icon} {discord_reminder_scheduled_msg}", 
                    inline=False
                )

            embed.set_footer(
                text=f"{embed_footer}",
                icon_url=self.bot.user.display_avatar.url if self.bot.user else None
            )

            await i.send(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Unexpected error in _process_remind for user {i.user.id}: {e}", exc_info=True)
            error_embed = nextcord.Embed(
                title="❌ Error",
                description="An unexpected error occurred while processing your reminder. Please try again later.",
                color=0xff0000
            )
            try:
                if not i.response.is_done():
                    await i.response.send_message(embed=error_embed, ephemeral=True)
                else:
                    await i.followup.send(embed=error_embed, ephemeral=True)
            except:
                pass

    @tasks.loop(seconds=15) # Check every 15 seconds
    async def check_reminders_loop(self):
        """
        Periodically checks for due reminders and sends them as Discord messages.
        
        This asynchronous loop runs at regular intervals, processes all reminders whose due time has passed, sends them to the appropriate Discord channels, and removes them from the pending list. Corrupt or malformed reminders are discarded. The updated reminders list is saved if any changes occur.
        """
        logger.debug("check_reminders_loop: Entered loop iteration.")
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        now_ts = now_utc.timestamp()
        logger.debug(f"check_reminders_loop: Current time: {now_utc.isoformat()} (TS: {now_ts}). Checking {len(self.reminders)} reminders.")
        
        reminders_to_keep = []
        reminders_processed_this_run = False

        for r_data in list(self.reminders): 
            due_timestamp = r_data.get("due_timestamp")
            reminder_id = r_data.get("id", "Unknown ID")
            logger.debug(f"Checking reminder: ID {reminder_id}, Due TS: {due_timestamp}, Original Str: '{r_data.get('original_time_str')}'")
            
            if not all(key in r_data for key in ["id", "user_id", "channel_id", "title", "message", "due_timestamp", "original_time_str"]):
                logger.error(f"Corrupt reminder data found in loop (missing keys), discarding: {reminder_id}. Data: {r_data}")
                reminders_processed_this_run = True
                continue 
            
            if not isinstance(due_timestamp, (int, float)):
                logger.error(f"Invalid due_timestamp type ({type(due_timestamp)}) in reminder, discarding: {reminder_id}. Data: {r_data}")
                reminders_processed_this_run = True
                continue

            if due_timestamp <= now_ts:
                due_dt_obj = datetime.datetime.fromtimestamp(due_timestamp, tz=datetime.timezone.utc)
                logger.info(f"Reminder ID {reminder_id} is due (Due: {due_dt_obj.isoformat()}, Now: {now_utc.isoformat()}). Attempting to send.")
                try:
                    await self._send_discord_reminder(r_data)
                    logger.info(f"Successfully processed and sent Discord reminder: {reminder_id}")
                except Exception as e: 
                    logger.error(f"Error sending Discord reminder {reminder_id}: {e}. Reminder removed to prevent retry loops.", exc_info=True)
                reminders_processed_this_run = True 
            else:
                reminders_to_keep.append(r_data)
        
        if reminders_processed_this_run:
            logger.debug(f"Reminders list changed. Old count: {len(self.reminders)}, New count: {len(reminders_to_keep)}. Saving.")
            self.reminders = reminders_to_keep
            self._save_reminders()
        elif len(self.reminders) > 0 :
             logger.debug(f"check_reminders_loop: No reminders processed in this iteration. {len(self.reminders)} reminders still pending.")

    @check_reminders_loop.before_loop
    async def before_check_reminders_loop(self):
        """
        Waits for the bot to become ready before starting the reminder checking loop.
        
        If an exception occurs during the wait, cancels the reminder checking loop.
        """
        try:
            logger.info("before_check_reminders_loop: Waiting for bot to be ready...")
            await self.bot.wait_until_ready()
            logger.info("before_check_reminders_loop: Bot is ready. Reminder check_reminders_loop is now officially starting.")
        except Exception as e:
            logger.error(f"CRITICAL: Exception in before_check_reminders_loop: {e}", exc_info=True)
            self.check_reminders_loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Handles the bot's on_ready event by ensuring the reminder checking loop is running.
        
        Starts the background task for checking and sending due reminders if it is not already active. Logs the status and any errors encountered during startup.
        """
        logger.info(f"Cog {self.__class__.__name__} received on_ready. Starting check_reminders_loop if not already running.")
        if not self.check_reminders_loop.is_running():
            try:
                self.check_reminders_loop.start()
                logger.info("check_reminders_loop started from on_ready.")
            except RuntimeError as e:
                logger.warning(f"Could not start check_reminders_loop from on_ready (possibly already started or other issue): {e}")
            except Exception as e:
                logger.error(f"Unexpected error starting check_reminders_loop from on_ready: {e}", exc_info=True)
        else:
            logger.info("check_reminders_loop was already running when on_ready was called.")

    def _parse_time_to_datetime(self, time_str: str, user_tz: str = None) -> datetime.datetime | None:
        """
        Parses a time string into a UTC datetime object, considering the user's timezone.
        
        Supports relative times (e.g., "10m", "2h", "1d", "30s"), absolute times (e.g., "16:30", "3pm"), and "tomorrow" prefixes. Returns a timezone-aware UTC datetime if parsing succeeds, or None if the format is invalid.
        
        Args:
            time_str: The time specification string to parse.
            user_tz: Optional IANA timezone string for the user. Defaults to UTC if not provided or invalid.
        
        Returns:
            A UTC datetime object representing the parsed time, or None if parsing fails.
        """
        if user_tz:
            try:
                tzinfo = zoneinfo.ZoneInfo(user_tz)
            except Exception:
                tzinfo = datetime.timezone.utc
        else:
            tzinfo = datetime.timezone.utc
        now = datetime.datetime.now(tzinfo)
        logger.debug(f"_parse_time_to_datetime: Input '{time_str}'. Current time ('now'): {now.isoformat()}")
        
        time_str_lower = time_str.lower().strip()

        patterns = [
            (r"(\d+)\s*s(?:ec(?:ond)?s?)?", datetime.timedelta(seconds=1)),
            (r"(\d+)\s*m(?:in(?:ute)?s?)?", datetime.timedelta(minutes=1)),
            (r"(\d+)\s*h(?:our(?:s)?)?", datetime.timedelta(hours=1)),
            (r"(\d+)\s*d(?:ay(?:s)?)?", datetime.timedelta(days=1)),
        ]

        for pattern, delta_unit in patterns:
            match = re.fullmatch(pattern, time_str_lower)
            if match:
                try:
                    value = int(match.group(1))
                    parsed_dt = now + delta_unit * value
                    logger.debug(f"Parsed '{time_str}' as relative time ({value} units of {delta_unit}) to: {parsed_dt.isoformat()}")
                    return parsed_dt.astimezone(datetime.timezone.utc)
                except ValueError:
                    logger.error(f"Could not convert '{match.group(1)}' to int for relative time parsing.")
                    return None

        base_date = now
        time_component_str = time_str_lower

        if time_str_lower.startswith("tomorrow"):
            base_date = now + datetime.timedelta(days=1)
            time_component_str = time_str_lower.replace("tomorrow", "", 1).strip()
            if not time_component_str:
                logger.debug(f"Parsed '{time_str}' as 'tomorrow' (same time as 'now') to: {base_date.isoformat()}")
                return base_date.astimezone(datetime.timezone.utc)

        match_time = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_component_str)
        if match_time:
            hour = int(match_time.group(1))
            minute = int(match_time.group(2) or 0)
            ampm = match_time.group(3)

            if ampm == "pm" and 1 <= hour <= 11:
                hour += 12
            elif ampm == "am" and hour == 12:
                hour = 0
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                 logger.warning(f"Invalid hour ({hour}) or minute ({minute}) from time_str: '{time_str}'")
                 return None

            try:
                target_dt = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                logger.debug(f"Initial target_dt for '{time_str}': {target_dt.isoformat()} (base_date: {base_date.isoformat()}, now: {now.isoformat()})")
                if target_dt <= now and base_date.date() == now.date():
                    logger.debug(f"Calculated time {target_dt.isoformat()} is in the past for today. Advancing to next day.")
                    target_dt += datetime.timedelta(days=1)
                logger.debug(f"Parsed '{time_str}' as absolute time to: {target_dt.isoformat()}")
                return target_dt.astimezone(datetime.timezone.utc)
            except ValueError as e:
                logger.error(f"ValueError during date replacement for '{time_str}': {e}", exc_info=True)
                return None
        
        if not time_component_str and base_date.date() > now.date():
             logger.debug(f"Parsed '{time_str}' (effectively only 'tomorrow') to: {base_date.isoformat()}")
             return base_date.astimezone(datetime.timezone.utc)

        logger.warning(f"Could not parse time_str: '{time_str}' into a datetime object using available patterns.")
        return None

    def _load_reminders(self):
        """
        Loads reminders from the cache file, filtering out malformed entries and initializing the active reminders list.
        
        If the cache file is missing or contains invalid data, starts with an empty reminders list.
        """
        logger.debug(f"Attempting to load reminders from {CACHE_FILE_PATH}")
        if os.path.exists(CACHE_FILE_PATH):
            try:
                with open(CACHE_FILE_PATH, 'r') as f:
                    loaded_reminders = json.load(f)
                
                valid_reminders = []
                malformed_count = 0
                if not isinstance(loaded_reminders, list):
                    logger.error(f"Reminders cache file {CACHE_FILE_PATH} does not contain a JSON list. Starting fresh.")
                    self.reminders = []
                    return

                for r_idx, r in enumerate(loaded_reminders):
                    if isinstance(r, dict) and isinstance(r.get("due_timestamp"), (int, float)) and r.get("id"):
                        valid_reminders.append(r)
                        due_dt_obj = datetime.datetime.fromtimestamp(r['due_timestamp'], tz=datetime.timezone.utc)
                        logger.debug(f"Loaded reminder from cache: ID {r['id']}, Due: {due_dt_obj.isoformat()}, OriginalStr: '{r.get('original_time_str')}'")
                    else:
                        malformed_count += 1
                        logger.warning(f"Malformed reminder data at index {r_idx} in cache: {r}")
                self.reminders = valid_reminders

                if malformed_count > 0:
                    logger.warning(f"Filtered out {malformed_count} malformed reminders during load.")
            except json.JSONDecodeError:
                logger.error(f"Error loading reminders cache from {CACHE_FILE_PATH}: Invalid JSON. Starting fresh.", exc_info=True)
                self.reminders = []
            except Exception as e:
                logger.error(f"Unexpected error loading reminders from {CACHE_FILE_PATH}: {e}. Starting fresh.", exc_info=True)
                self.reminders = []
        else:
            logger.info(f"Reminders cache file {CACHE_FILE_PATH} not found. Starting with no reminders.")
            self.reminders = []
        logger.info(f"Finished loading. {len(self.reminders)} reminders are active.")

    def _save_reminders(self):
        """
        Saves the current list of reminders to the persistent JSON cache file.
        
        Logs success or error details during the save operation.
        """
        logger.debug(f"Attempting to save {len(self.reminders)} reminders to {CACHE_FILE_PATH}.")
        try:
            with open(CACHE_FILE_PATH, 'w') as f:
                json.dump(self.reminders, f, indent=4)
            logger.info(f"Successfully saved {len(self.reminders)} reminders to {CACHE_FILE_PATH}.")
        except IOError as e:
            logger.error(f"IOError saving reminders cache to {CACHE_FILE_PATH}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error saving reminders to {CACHE_FILE_PATH}: {e}", exc_info=True)

    @nextcord.slash_command(name="remind", description="Set a reminder for yourself")
    async def remind(self,
                     i: Interaction,
                     message: str = SlashOption(description="What do you want to be reminded about?", required=True),
                     time: str = SlashOption(description="When? (e.g. '10m', '2h', '1d', 'tomorrow 3pm', '17:00')", required=True),
                     title: str = SlashOption(description="What should the title be?", required=False),
                     topic: str = SlashOption(description="What is the ntfy topic? (default: 'reminders')", required=False),
                     channel: TextChannel = SlashOption(description="Channel for Discord reminder (defaults to current)", required=False, default=None)
                     ):
        """
                     Handles the `/remind` slash command to schedule a reminder with optional ntfy notification.
                     
                     Prompts the user to set their timezone if not already configured, deferring reminder creation until the timezone is set. Otherwise, processes the reminder immediately with the provided details.
                     """
                     user_tz = self._get_user_timezone(i.user.id)
        if not user_tz:
            # Save the original arguments for later processing
            args = dict(i=i, message=message, time=time, title=title, topic=topic, channel=channel)
            await self._ask_timezone(i, lambda inter, tz: self._on_timezone_set(inter, tz), pending_args=args)
            return
        # If timezone is set, process as normal
        await self._process_remind(i=i, message=message, time=time, title=title, topic=topic, channel=channel)

    async def _send_discord_reminder(self, reminder_data: dict):
        """
        Sends a scheduled reminder as an embedded message to the specified Discord text channel.
        
        Attempts to resolve the target channel and user, constructs a reminder embed, and mentions the user in the channel. Handles missing channels, users, and permission errors gracefully, logging any issues encountered.
        """
        reminder_id = reminder_data['id']
        user_id = reminder_data['user_id']
        channel_id = reminder_data['channel_id']
        guild_id = reminder_data.get("guild_id")

        logger.info(f"Preparing to send Discord reminder ID: {reminder_id}, User: {user_id}, Channel: {channel_id}, Guild: {guild_id}")
        logger.debug(f"Full reminder data for sending: {reminder_data}")

        target_channel = self.bot.get_channel(channel_id)
        
        if not target_channel and guild_id:
            guild = self.bot.get_guild(guild_id)
            if guild:
                logger.debug(f"Channel {channel_id} not in cache. Attempting to fetch from guild {guild.id}")
                try:
                    target_channel = await guild.fetch_channel(channel_id)
                except nextcord.NotFound:
                    logger.error(f"Channel {channel_id} not found in guild {guild.id} for reminder {reminder_id}.")
                except nextcord.Forbidden:
                    logger.error(f"Forbidden to fetch channel {channel_id} from guild {guild.id} for reminder {reminder_id}.")
                except nextcord.HTTPException as e:
                    logger.error(f"HTTPException fetching channel {channel_id} from guild {guild.id}: {e}")
        
        user = None
        if guild_id:
            guild = self.bot.get_guild(guild_id)
            if guild:
                logger.debug(f"Attempting to fetch member {user_id} from guild {guild.id}")
                try:
                    user = await guild.fetch_member(user_id) 
                except nextcord.NotFound:
                    logger.warning(f"Member {user_id} not found in guild {guild.id} for reminder {reminder_id}.")
                except nextcord.Forbidden:
                     logger.warning(f"Forbidden to fetch member {user_id} from guild {guild.id}.")
                except nextcord.HTTPException as e:
                    logger.error(f"HTTPException fetching member {user_id} from guild {guild.id}: {e}")

        if not user: 
            logger.debug(f"Member not found in guild or no guild_id. Attempting to fetch user {user_id} globally.")
            try:
                user = await self.bot.fetch_user(user_id) 
            except nextcord.NotFound:
                 logger.warning(f"User {user_id} not found globally for reminder {reminder_id}.")
            except nextcord.HTTPException as e:
                logger.error(f"HTTPException fetching user {user_id} globally: {e}")

        if not target_channel:
            logger.error(f"Could not find or fetch channel {channel_id} for reminder {reminder_id}. Reminder lost.")
            return
        if not isinstance(target_channel, TextChannel): 
            logger.error(f"Channel {channel_id} for reminder {reminder_id} is not a TextChannel (type: {type(target_channel)}). Reminder lost.")
            return
            
        user_mention_str = f"<@{user_id}>" 
        if user:
            user_mention_str = user.mention
        else:
            logger.warning(f"Could not find user object for {user_id} for reminder {reminder_id}. Using raw ID mention.")

        embed = Embed(
            title=f"⏰ Reminder: {reminder_data['title']}",
            description=reminder_data['message'],
            color=Color.blue(), 
            timestamp=datetime.datetime.fromtimestamp(reminder_data['due_timestamp'], tz=datetime.timezone.utc)
        )
        original_time_display = reminder_data.get('original_time_str', 'N/A')
        embed.set_footer(
            text=f"{embed_footer} | Originally set for: '{original_time_display}'",
            icon_url=self.bot.user.display_avatar.url if self.bot.user else None
        )
        
        try:
            logger.info(f"Sending reminder embed to channel {target_channel.id} ({target_channel.name}) for user {user_mention_str} (Reminder ID: {reminder_id})")
            await target_channel.send(content=f"{user_mention_str}, here's your reminder!", embed=embed)
            logger.info(f"Successfully sent reminder ID {reminder_id} to channel {target_channel.id}.")
        except nextcord.Forbidden:
            logger.error(f"Failed to send reminder {reminder_id} to channel {target_channel.id} ({target_channel.name}): Missing permissions (Forbidden).", exc_info=True)
        except nextcord.HTTPException as e:
            logger.error(f"Failed to send reminder {reminder_id} to channel {target_channel.id} ({target_channel.name}): HTTP Exception {e.status} - {e.text}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending reminder {reminder_id} to {target_channel.id}: {e}", exc_info=True)

def setup(bot):
    """
    Initializes and adds the ReminderCommand cog to the Discord bot.
    
    Logs the setup process and any errors encountered during cog addition.
    """
    logger.info("Setting up ReminderCommand cog.")
    try:
        bot.add_cog(ReminderCommand(bot))
        logger.info("ReminderCommand cog added successfully.")
    except Exception as e:
        logger.error(f"Failed to add ReminderCommand cog: {e}", exc_info=True)
