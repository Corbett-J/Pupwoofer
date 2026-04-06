import functools
import json

import discord
from discord.ext import commands

from config import SAVE_FILE_PATH

from utils.permissions import user_has_pemission
from utils.messages import send_initial_message

from commands.ryo_stop import ryo_stop
from commands.ryo_start import ryo_start
from commands.ryo_backup import ryo_backup
from commands.ryo_update import ryo_update

class RyokonomasKingdom(commands.GroupCog, group_name="ryo"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="stop", description="Stops the Ryokonoma's Kingdom server.")
    @user_has_pemission("ryokonomas_kingdom")
    async def stop(self, interaction: discord.Interaction):
        if self.bot.ryokonomas_kingdom_server_process is None:
            await send_initial_message(interaction, "The server seems to already be stopped.")
            return
        message = await send_initial_message(interaction, "bork...")
        self.bot.ryokonomas_kingdom_server_process = await ryo_stop(self.bot.ryokonomas_kingdom_server_process)
        await message.channel.send("bork bork!")
        return
    
    @discord.app_commands.command(name="start", description="Starts the Ryokonoma's Kingdom server.")
    @user_has_pemission("ryokonomas_kingdom")
    async def start(self, interaction: discord.Interaction):
        if self.bot.ryokonomas_kingdom_server_process is not None:
            await send_initial_message(interaction, "The server seems to already be started.")
            return
        message = await send_initial_message(interaction, "bork...")
        with open(SAVE_FILE_PATH, 'r') as save_file:
            save_data = json.load(save_file)
        current_version_name = save_data["minecraft_bedrock"]["current_version_name"]
        self.bot.ryokonomas_kingdom_server_process = await ryo_start(self.bot.ryokonomas_kingdom_server_process, current_version_name)
        await message.channel.send("bork bork!")
        return
    
    @discord.app_commands.command(name="restart", description="Restarts the Ryokonoma's Kingdom server.")
    @user_has_pemission("ryokonomas_kingdom")
    async def restart(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "bork...")
        self.bot.ryokonomas_kingdom_server_process = await ryo_stop(self.bot.ryokonomas_kingdom_server_process)
        with open(SAVE_FILE_PATH, 'r') as save_file:
            save_data = json.load(save_file)
        current_version_name = save_data["minecraft_bedrock"]["current_version_name"]
        self.bot.ryokonomas_kingdom_server_process = await ryo_start(self.bot.ryokonomas_kingdom_server_process, current_version_name)
        await message.channel.send("bork bork!")
        return

    @discord.app_commands.command(name="backup", description="Creates a backup of the Ryokonoma's Kingdom server.")
    @user_has_pemission("ryokonomas_kingdom")
    async def backup(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "borkup starting, closing server...")
        self.bot.ryokonomas_kingdom_server_process = await ryo_stop(self.bot.ryokonomas_kingdom_server_process)
        await message.channel.send("borking up...")
        with open(SAVE_FILE_PATH, 'r') as save_file:
             save_data = json.load(save_file)
        current_version_name = save_data["minecraft_bedrock"]["current_version_name"]
        ryo_backup(current_version_name)
        await message.channel.send("borkup complete! Starting server...")
        self.bot.ryokonomas_kingdom_server_process = await ryo_start(self.bot.ryokonomas_kingdom_server_process, current_version_name)
        await message.channel.send("bork bork!")
    
    @discord.app_commands.command(name="update", description="Updates the the Ryokonoma's Kingdom server to the latest version of Minecraft Bedrock Edition.")
    @user_has_pemission("ryokonomas_kingdom")
    async def update(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "borkup starting!")
        await message.channel.send("closing server...")
        self.bot.ryokonomas_kingdom_server_process = await ryo_stop(self.bot.ryokonomas_kingdom_server_process)
        await message.channel.send("borking up...")
        with open(SAVE_FILE_PATH, 'r') as save_file:
            save_data = json.load(save_file)
        old_version_name = save_data["minecraft_bedrock"]["current_version_name"]
        backup_date_time = ryo_backup(old_version_name)
        await message.channel.send(f"borkup complete! Updating from version '{old_version_name}'. Downloading update, this may take a few minutes...")
        new_version_name = await self.bot.loop.run_in_executor(None, functools.partial(ryo_update, backup_date_time, old_version_name))
        if "error" in new_version_name:
            await message.channel.send(f"update failed, grrr! Failed to update to version '{new_version_name}'.")
            return
        with open(SAVE_FILE_PATH, 'w') as save_file:
            save_data["minecraft_bedrock"] = {
                "current_version_name": new_version_name,
            }
            json.dump(save_data, save_file, ensure_ascii=False, indent=4)
        await message.channel.send(f"borkdate complete! Updated to version '{new_version_name}'. Starting server...")
        ryo_start(self.bot.ryo_server_process, new_version_name)
        await message.channel.send("bork bork!")
        return

async def setup(bot):
    await bot.add_cog(RyokonomasKingdom(bot))