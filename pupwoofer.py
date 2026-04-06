import asyncio
import discord
from discord.ext import commands
import logging
import traceback
import json

from config import SAVE_FILE_PATH, SECRETS_FILE_PATH

from commands.ryo_start import ryo_start
from commands.ryo_stop import ryo_stop

logger = logging.getLogger("discord")
logging.basicConfig(level=logging.WARNING)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


class Pupwoofer(commands.Bot):
    def __init__(self, *args, developer_discord_user_id: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.developer_discord_user_id: int = developer_discord_user_id
        self.ryokonomas_kingdom_server_process: asyncio.subprocess.Process | None = None
        self.ryokonomas_kingdom_auto_backup_loop = None

    async def setup_hook(self):
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.developer")
        await self.load_extension("cogs.kpop")
        await self.load_extension("cogs.local")
        await self.load_extension("cogs.ryokonomas_kingdom")
        await self.load_extension("cogs.valheim")
        await self.load_extension("services.ryokonomas_kingdom_auto_backup")

        loaded_extension_names = self.extensions.keys()
        print(f"loaded {len(loaded_extension_names)} extensions:")
        for loaded_extension_name in loaded_extension_names:
            print(f"- {loaded_extension_name}")

        synced_commands = await self.tree.sync()
        print(f"Synced {len(synced_commands)} commands:")
        for synced_command in synced_commands:
            print(f"- {synced_command.name}")
        
        with open(SAVE_FILE_PATH, "r") as save_file:
            save_data = json.load(save_file)
        self.ryokonomas_kingdom_server_process = await ryo_start(
            self.ryokonomas_kingdom_server_process,
            save_data["minecraft_bedrock"]["current_version_name"],
        )

    async def on_ready(self):
        print(f"{self.user} is logged on!")
        await self.change_presence(activity=discord.Activity(name="Waiting to help"))

        with open(SAVE_FILE_PATH, "r") as save_file:
            save_data = json.load(save_file)

        if save_data["restart_state"]["restart_started"]:
            channel = self.get_channel(save_data["restart_state"]["channel_started_from_id"])
            with open(SAVE_FILE_PATH, "w") as save_file:
                save_data["restart_state"] = {"restart_started": False}
                json.dump(save_data, save_file, ensure_ascii=False, indent=4)
            await channel.send("server reborked!")
        else:
            developer_discord_user = await self.fetch_user(self.developer_discord_user_id)
            await developer_discord_user.send("I'm awake!")

    async def on_app_command_error(self, interaction: discord.Interaction, error):
        developer_discord_user = await self.fetch_user(self.developer_discord_user_id)
        await developer_discord_user.send(
            f"An error occurred\nInteraction: '{str(interaction)}'\n"
            f"Error: {error}\nTraceback: {traceback.format_tb(error.__traceback__)}"
        )

        if isinstance(error, discord.app_commands.errors.CheckFailure):
            await interaction.response.send_message(
                "Grr... you don't have permission to use this command.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Grr... Something unexpected went wrong. I'll tell <@{self.developer_discord_user_id}>",
                ephemeral=True,
            )

    async def graceful_shutdown(self, self_restart = False):
        print("Gracefully shutting down")
        if self.ryokonomas_kingdom_server_process:
            self.ryokonomas_kingdom_server_process = await ryo_stop(
                self.ryokonomas_kingdom_server_process
            )
        developer_discord_user = await self.fetch_user(self.developer_discord_user_id)
        await developer_discord_user.send("Shutting down")
        if self_restart:
            pass
        else:
            await super().close()

async def main():
    with open(SECRETS_FILE_PATH, "r") as secrets_file:
            secrets = json.load(secrets_file)
    discord_bot_token = secrets["discord_bot_token"]
    developer_discord_user_id = secrets["developer_discord_user_id"]

    intents = discord.Intents.default()
    intents.message_content = True
      
    bot = Pupwoofer(
        command_prefix="/",
        intents=intents,
        developer_discord_user_id=developer_discord_user_id,
    )
    try:
        await bot.start(discord_bot_token)
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        print("KeyboardInterrupt or asyncio.exceptions.CancelledError received")
    finally:
        await bot.graceful_shutdown()
        if not bot.is_closed():
            await bot.close()

asyncio.run(main())
