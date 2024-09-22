import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color


class Recieved(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='recieved', description='Returns total emojis recieved for said emoji')
    @app_commands.describe(emoji='The emoji to query about')
    async def recieved(
        self,
        interaction: discord.Interaction,
        emoji: str
    ):
        data = returnJsonResponse(f'command/recieved/{emoji}')

        if len(data):
            data = '\n'.join(row[0] for row in data)
        else:
            data = 'No data recorded'

        embed = create_embed(f'Total Emojis Recieved For: {emoji}', data, random_color()) 
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Recieved(bot))
