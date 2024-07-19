import discord
from discord.ext import commands
from discord import app_commands
import random

class RandomNumCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='random_num_gen', description='Pick a random number between the two choices')
    @app_commands.describe(begin_num='Lowest Number', end_num='Highest Number')
    async def rng(
        self,
        interaction: discord.Interaction,
        begin_num: app_commands.Range[int, 0, None],
        end_num: app_commands.Range[int, 0, None],
    ):
        if begin_num > end_num:
            await interaction.response.send_message(f'{interaction.user.mention}, your end number is larger than your beginning number.')
        else:
            await interaction.response.send_message(f'{interaction.user.mention}, your number is {random.randint(begin_num, end_num)}')

async def setup(bot):
    await bot.add_cog(RandomNumCommand(bot))
