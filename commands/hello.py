import discord
from discord import app_commands
from discord.ext import commands

class HelloCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='hello', description='Says hi to the peasants')
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')

async def setup(bot: commands.Bot):
    await bot.add_cog(HelloCommand(bot))