import discord
from discord.ext import commands
from discord import app_commands
import random
from utils.helper import create_embed, random_color

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
            embed = create_embed(f'{interaction.user.mention}, your end number is larger than your beginning number.', '', random_color()) 
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            embed = create_embed(f'Your random number is:', f'{random.randint(begin_num, end_num)}', random_color()) 
            await interaction.response.send_message(embed=embed, ephemeral=False)
            #await interaction.response.send_message(f'{interaction.user.mention}, your number is {random.randint(begin_num, end_num)}')

async def setup(bot):
    await bot.add_cog(RandomNumCommand(bot))
