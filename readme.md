# Pluto Discord Bot

## What is Pluto?
Pluto is a personal Discord bot designed to manage servers, provide fun and utility commands, and automate common tasks. Originally for personal use, Pluto has grown to include a wide range of features and may become public in the future.

---

## Features

### Moderation
- **Kick/Ban Members**: Remove problematic users from your server.
- **Clear/Purge Messages**: Bulk delete messages or purge entire channels.
- **NSFW Content Restriction**: NSFW commands only work in NSFW channels.

### Fun & Entertainment
- **Roast Me**: Get a random roast from a curated list.
- **Random Dog Pictures**: Fetches random dog images from a public API.
- **Random Cat Pictures**: Fetches random cat images from a public API.
- **Random Jokes**: Get a random joke from an online API.
- **NSFW Hentai**: Fetches NSFW images/GIFs from Purrbot (works only in NSFW channels).

### Information
- **User Info**: Get detailed information about a user (join date, roles, avatar, etc.).
- **Avatar**: Display a user's avatar.
- **Bot Info**: Information about Pluto, including stats and author.
- **System Info**: View system load, memory, CPU, and disk usage.

### Utilities
- **Reminders**: Set reminders for yourself, with support for timezones and instant reminders. Reminders can be sent both in Discord and via ntfy notifications.
- **Run Command**: `/run` (owner only) – run shell commands directly from Discord (with safety checks).
- **Time Test**: See the current UTC and CET time.

### Help & Error Handling
- **Help Menu**: Paginated help command listing all available commands.
- **Command Info**: Get detailed info about a specific command.
- **Automatic Error Reporting**: Errors are reported and can be sent to GitHub as issues (if configured and set up properly (that includes setting up a github bot and a personal access token)).

---

## Example Commands
| Command                                           | Description                                 |
| ------------------------------------------------- | ------------------------------------------- |
| `/kick <member> [reason]`                         | Kick a user                                 |
| `/ban <member> [reason]`                          | Ban a user                                  |
| `/clear <amount>`                                 | Delete a number of messages                 |
| `/purge`                                          | Purge all messages in a channel             |
| `/roastme`                                        | Get roasted                                 |
| `/dog`                                            | Random dog picture                          |
| `/cat`                                            | Random cat picture                          |
| `/joke`                                           | Random joke                                 |
| `/hentai <category>`                              | NSFW image/gif (NSFW channels only)         |
| `/userinfo [user]`                                | Info about a user                           |
| `/avatar [user]`                                  | Show a user's avatar                        |
| `/about`                                          | Info about Pluto                            |
| `/systeminfo`                                     | System stats                                |
| `/remind <message> <time> [title] [topic] [channel]` | Set a reminder (supports instant reminders with `0`) |
| `/run <command>`                                  | Run a shell command (owner only)            |
| `/help`                                           | Show all commands                           |
| `/commandinfo <command>`                          | Info about a specific command               |

---

## Planned Features (I don't know when)
- **Music Functionality**: Spotify/Youtube playback and music bot features.
- **Configurable Chat Log**: Set log channels for deleted messages via command.

---

## What Pluto Will Not Do
- Explain the aerodynamics of a cow.

---

## Notes
- Some commands are restricted to server admins or the bot owner.
- NSFW commands require an NSFW channel.
- Error handling is robust and can create GitHub issues for unhandled exceptions (if configured correctly).

---

## Author
- Made by [`alexdot`](https://github.com/unfortunatelyalex)
