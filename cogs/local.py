import discord
from discord.ext import commands

from utils.permissions import user_has_pemission
from utils.messages import send_initial_message

from commands.get_local_ip import get_local_ip

class Local(commands.GroupCog, group_name="local"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="getip", description="Gets the local ip of the server.")
    @user_has_pemission("local")
    async def stop(self, interaction: discord.Interaction):
        local_ip = get_local_ip()
        await send_initial_message(interaction, local_ip)
        return

async def setup(bot):
    await bot.add_cog(Local(bot))