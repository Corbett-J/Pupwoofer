import json
import discord
from discord.ext import commands

from config import SAVE_FILE_PATH

from utils.messages import send_initial_message
from utils.permissions import user_has_pemission

from commands.fix_server import fix_server
from commands.restart_server import restart_server


class Admin(commands.GroupCog, group_name="admin"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="fixserver", description="Restarts the playit.gg service")
    @user_has_pemission("admin")
    async def reload_extension(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "bork...")
        fix_server()
        await message.channel.send("bork bork!")
    
    @discord.app_commands.command(name="restartserver", description="Restarts the entire server PC (windows restart)")
    @user_has_pemission("admin")
    async def reload_extension(self, interaction: discord.Interaction):
        await send_initial_message(interaction, "This command is currently disabled, as the desktop is not reloaded on startup, so none of the server processess start up, and so the server is effectively just taken offline.")
        return
        message = await send_initial_message(interaction,"reborking...")
        with open('SAVE_FILE_PATH', 'r') as save_file:
            save_data = json.load(save_file)

        with open('SAVE_FILE_PATH', 'w') as save_file:
            save_data["restart_state"] = {
                "restart_started": True,
                "channel_started_from_id": message.channel.id
            }
            json.dump(save_data, save_file, ensure_ascii=False, indent=4)

        restart_server()

async def setup(bot):
    await bot.add_cog(Admin(bot))