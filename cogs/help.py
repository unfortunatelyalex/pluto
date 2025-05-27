import nextcord
import math
from nextcord import Interaction, ButtonStyle
from nextcord.ext import commands
from nextcord.ui import View, Button
from main import embed_footer


class HelpView(View):
    def __init__(self, bot, interaction_user):
        super().__init__(timeout=180)
        self.bot = bot
        self.interaction_user = interaction_user
        self.current_page = 0
        self.commands_per_page = 24  # Safe limit under 25 fields (leaving 1 for footer/header info)
        
        # Get all commands and organize by category
        all_commands = sorted(self.bot.get_all_application_commands(), key=lambda cmd: cmd.name)
        self.commands = all_commands
        self.max_pages = math.ceil(len(self.commands) / self.commands_per_page)
        
        # Update button states
        self.update_buttons()
    
    def update_buttons(self):
        self.clear_items()
        
        # Previous button
        prev_button = Button(
            label="◀ Previous", 
            style=ButtonStyle.secondary, 
            disabled=self.current_page <= 0
        )
        prev_button.callback = self.previous_page
        self.add_item(prev_button)
        
        # Page indicator
        page_button = Button(
            label=f"Page {self.current_page + 1}/{self.max_pages}",
            style=ButtonStyle.primary,
            disabled=True
        )
        self.add_item(page_button)
        
        # Next button
        next_button = Button(
            label="Next ▶", 
            style=ButtonStyle.secondary, 
            disabled=self.current_page >= self.max_pages - 1
        )
        next_button.callback = self.next_page
        self.add_item(next_button)
    
    def create_embed(self):
        start_idx = self.current_page * self.commands_per_page
        end_idx = min(start_idx + self.commands_per_page, len(self.commands))
        page_commands = self.commands[start_idx:end_idx]
        
        embed = nextcord.Embed(
            title="📚 Command Help",
            description=f"Here are all available commands (Page {self.current_page + 1}/{self.max_pages})",
            color=0x00ff00
        )
        
        # Add each command as a separate field to avoid 1024 character limit
        field_count = 0
        for command in page_commands:
            if field_count >= 25:  # Discord's field limit
                break
                
            try:
                command_mention = command.get_mention() if hasattr(command, 'get_mention') else f"/{command.name}"
                description = command.description or "No description available"
                
                # Truncate description if it's too long (leaving room for command mention)
                max_desc_length = 950  # Safe limit under 1024
                if len(description) > max_desc_length:
                    description = description[:max_desc_length-3] + "..."
                
                # Get cog name for organization
                cog_name = command.cog_name if hasattr(command, 'cog_name') and command.cog_name else "General"
                
                embed.add_field(
                    name=f"{command_mention}",
                    value=f"**Category:** {cog_name}\n{description}",
                    inline=True
                )
                field_count += 1
                
            except Exception as e:
                # Fallback for commands that might not have get_mention()
                description = command.description or "No description available"
                if len(description) > 950:
                    description = description[:947] + "..."
                    
                embed.add_field(
                    name=f"/{command.name}",
                    value=description,
                    inline=True
                )
                field_count += 1
        
        embed.set_footer(text=f"{embed_footer} | Total Commands: {len(self.commands)}")
        return embed
    
    async def previous_page(self, interaction: Interaction):
        if interaction.user != self.interaction_user:
            await interaction.response.send_message("You can't control this help menu!", ephemeral=True)
            return
            
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()
    
    async def next_page(self, interaction: Interaction):
        if interaction.user != self.interaction_user:
            await interaction.response.send_message("You can't control this help menu!", ephemeral=True)
            return
            
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()
    
    async def on_timeout(self):
        # Disable all buttons when the view times out
        for item in self.children:
            item.disabled = True


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(force_global=True, description="Shows all the commands available")
    async def help(self, i: Interaction):
        view = HelpView(self.bot, i.user)
        embed = view.create_embed()
        await i.response.send_message(embed=embed, view=view)
    
    @nextcord.slash_command(name="commandinfo", description="Get detailed information about a specific command")
    async def command_info(self, i: Interaction, command_name: str):
        # Find the command
        all_commands = self.bot.get_all_application_commands()
        target_command = None
        
        for command in all_commands:
            if command.name.lower() == command_name.lower():
                target_command = command
                break
        
        if not target_command:
            embed = nextcord.Embed(
                title="❌ Command Not Found",
                description=f"No command named `{command_name}` was found.",
                color=0xff0000
            )
            await i.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = nextcord.Embed(
            title=f"📖 Command: {target_command.name}",
            description=target_command.description or "No description available",
            color=0x00ff00
        )
        
        # Add command details
        embed.add_field(name="Usage", value=f"/{target_command.name}", inline=True)
        embed.add_field(name="Category", value=target_command.cog_name if hasattr(target_command, 'cog_name') else "General", inline=True)
        
        # Add parameters if any
        if hasattr(target_command, 'options') and target_command.options:
            param_list = []
            for option in target_command.options:
                try:
                    # Check if option is a proper option object with required attribute
                    if hasattr(option, 'required') and hasattr(option, 'name'):
                        required = "Required" if option.required else "Optional"
                        option_type = getattr(option, 'type', 'Unknown')
                        type_name = getattr(option_type, 'name', str(option_type))
                        param_list.append(f"`{option.name}` ({type_name}) - {required}")
                    elif hasattr(option, 'name'):
                        # Fallback for options without required attribute
                        option_type = getattr(option, 'type', 'Unknown')
                        type_name = getattr(option_type, 'name', str(option_type))
                        param_list.append(f"`{option.name}` ({type_name}) - Optional")
                    else:
                        # Fallback for string or other unexpected types
                        param_list.append(f"`{str(option)}` - Unknown")
                except Exception as e:
                    # Ultimate fallback for any unexpected option format
                    param_list.append(f"`{str(option)}` - Unknown")
            
            if param_list:
                embed.add_field(name="Parameters", value="\n".join(param_list), inline=False)
        
        embed.set_footer(text=embed_footer)
        await i.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
