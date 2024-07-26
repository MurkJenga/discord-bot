import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color


class Given(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='given', description='Returns total emojis given for said emoji')
    @app_commands.describe(emoji='The first number to add')
    async def given(
        self,
        interaction: discord.Interaction,
        emoji: str
    ):
        data = returnJsonResponse(f'emoji/given/{emoji}')

        if len(data):
            data = '\n'.join(row['stats'] for row in data)
        else:
            data = 'No data recorded'

        embed = create_embed(f'Total Emojis Given For: {emoji}', data, random_color()) 
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Given(bot))
