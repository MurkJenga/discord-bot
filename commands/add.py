import discord
from discord.ext import commands
from discord import app_commands

class AddCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add', description='Add two numbers')
    @app_commands.describe(first='The first number to add', second='The second number to add')
    async def add(
        self,
        interaction: discord.Interaction,
        first: app_commands.Range[int, 0, 100],
        second: app_commands.Range[int, 0, None],
    ):
        """Adds two numbers together"""
        await interaction.response.send_message(f'{first} + {second} = {first + second}', ephemeral=False)

async def setup(bot):
    await bot.add_cog(AddCommand(bot))
