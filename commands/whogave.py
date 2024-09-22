import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color


class WhoGave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='whogave', description='See who gave the most amount of emojis to the specified user')
    @app_commands.describe(emoji='The emoji to query about', user='The user to check')
    async def whogave(
        self,
        interaction: discord.Interaction,
        emoji: str,
        user: discord.Member
    ):
        data = returnJsonResponse(f'command/whogave/{user.id}/{emoji}') 
        
        if data:
            data = '\n'.join(row[0] for row in data)
        else:
            data = 'No data recorded'

        embed = create_embed(f'Total {emoji} Given To {user.name}', data, random_color()) 
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(WhoGave(bot))
