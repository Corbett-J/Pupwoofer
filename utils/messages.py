import discord

async def send_initial_message(interaction: discord.Interaction, text_to_send: str) -> discord.Message:
    await interaction.response.send_message(text_to_send)
    return await interaction.original_response()
