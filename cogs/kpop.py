import discord
from discord.ext import commands

from config import SAVE_FILE_PATH

from utils.permissions import user_has_pemission
from utils.messages import send_initial_message

from commands.get_kpop_news import get_kpop_news

class Kpop(commands.GroupCog, group_name="kpop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="getnews", description="Gets the latest kpop news on demand.")
    @user_has_pemission("kpop")
    async def stop(self, interaction: discord.Interaction):
        initial_message = await send_initial_message(interaction, "bork! searching...")
        article_links = get_kpop_news(SAVE_FILE_PATH)
        follow_up_message = ""
        for article_link in article_links:
            follow_up_message = follow_up_message + f"- {article_link}\n"
            if len(follow_up_message) > 1600:
                initial_message.channel.send(follow_up_message)
                follow_up_message = ""     
        if follow_up_message:
            initial_message.channel.send(follow_up_message)

        

async def setup(bot):
    await bot.add_cog(Kpop(bot))