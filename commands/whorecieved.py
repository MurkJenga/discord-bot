import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color


class WhoRecieved(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='whorecieved', description='Returns list of users the specified user gave the emoji to')
    @app_commands.describe(emoji='The emoji to query about', user='The user to check')
    async def whorecieved(
        self,
        interaction: discord.Interaction,
        emoji: str,
        user: discord.Member
    ):
        data = returnJsonResponse(f'command/whorecieved/{user.id}/{emoji}') 
        
        if data:
            data = '\n'.join(row[0] for row in data)
        else:
            data = 'No data recorded'

        embed = create_embed(f'Total {emoji} Recieved From {user.name}', data, random_color()) 
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(WhoRecieved(bot))
