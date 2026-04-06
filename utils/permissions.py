import json
import discord
from discord import app_commands

from config import SECRETS_FILE_PATH

def user_has_pemission(key: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        with open(SECRETS_FILE_PATH, "r") as secrets_file:
            secrets = json.load(secrets_file)
        permissions = secrets["permissions"]
        
        is_user_permitted = (
            interaction.user.id in permissions[key]
            or
            interaction.user.id in permissions["owner"]
        )

        return is_user_permitted
    
    return app_commands.check(predicate)
