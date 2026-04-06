import discord
from discord.ext import commands

from utils.messages import send_initial_message
from utils.permissions import user_has_pemission

from commands.valheim_stop import valheim_stop
from commands.valheim_start import valheim_start
from commands.valheim_update import valheim_update


class Valheim(commands.GroupCog, group_name="valheim"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @discord.app_commands.command(name="stop", description="Stops the Valheim server.")
    @user_has_pemission("valheim")
    async def stop(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "bork, stopping server...")
        valheim_stop()
        await message.channel.send("bork bork!")
        return
    
    @discord.app_commands.command(name="start", description="Starts the Valheim server.")
    @user_has_pemission("valheim")
    async def start(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "bork, starting server...")
        valheim_start()
        await message.channel.send("bork bork!")
        return
    
    @discord.app_commands.command(name="update", description="Updates the Valheim server to the latest version of the public-test branch.")
    @user_has_pemission("valheim")
    async def update(self, interaction: discord.Interaction):
        message = await send_initial_message(interaction, "borkdate starting, closing server...")
        valheim_stop()
        await message.channel.send("borkdateing... (This may take several minutes)")
        valheim_update()
        await message.channel.send("borkdate complete! Starting server...")
        valheim_start()
        await message.channel.send("bork bork!")
        return

async def setup(bot):
    await bot.add_cog(Valheim(bot))