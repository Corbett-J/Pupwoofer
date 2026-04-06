import os
import sys
import discord
from discord.ext import commands

from utils.messages import send_initial_message
from utils.permissions import user_has_pemission


class Developer(commands.GroupCog, group_name="developer"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="reloadextension", description="Reloads an extension")
    @discord.app_commands.describe(extension="Choose an extension")
    @user_has_pemission("developer")
    async def reload_extension(self, interaction: discord.Interaction, extension: str):
        message = await send_initial_message(interaction, f"bork, reloading {extension}...")
        await self.bot.reload_extension(extension)
        await message.channel.send(f"extension reloaded! Syncing command tree...")
        synced = await self.bot.tree.sync()
        await message.channel.send(f"bork bork! Synced commands:\n{synced}")
        return
    
    @discord.app_commands.command(name="loadextension", description="Loads an extension")
    @discord.app_commands.describe(extension="Choose an extension")
    @user_has_pemission("developer")
    async def load_extension(self, interaction: discord.Interaction, extension: str):
        message = await send_initial_message(interaction, f"bork, loading {extension}...")
        await self.bot.load_extension(extension)
        await message.channel.send(f"extension loaded! Syncing command tree...")
        synced = await self.bot.tree.sync()
        message.channel.send(f"bork bork! Synced commands:\n{synced}")
        return
    
    @discord.app_commands.command(name="restartpupwoofer", description="Restarts the Pupwoofer discord bot, inlcuding subprocesses such as the Minecraft Bedrock server")
    @user_has_pemission("admin")
    async def restart_pupwoofer(self, interaction: discord.Interaction):
        await self.bot.graceful_shutdown(self_restart=True)
        await send_initial_message(interaction,"zzzzzz...")
        os.execv(sys.executable, ['python'] + sys.argv)

    @reload_extension.autocomplete("extension")
    async def reload_extension_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
        ):
            return [
                discord.app_commands.Choice(name=name, value=name)
                for name in self.bot.extensions
                if current.lower() in name.lower()
            ]
    
async def setup(bot):
    await bot.add_cog(Developer(bot))