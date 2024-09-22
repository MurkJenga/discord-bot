import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color, get_date
import re
from typing import Optional

class Total(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='total', description='Returns total messages per user by specific date')
    @app_commands.describe(date='The date to see total messages')
    async def total(
        self,
        interaction: discord.Interaction,
        date: Optional[str] = None
    ): 
        if date is None:
            date = get_date()  
        
        def validate_date(date):
            reg = '^\\d{4}-\\d{2}-\\d{2}$'
            return date if re.search(reg, date) else None
        
        if validate_date(date): 
            data = returnJsonResponse(f'command/total/{date}') 
            if len(data):
                data =  '\n'.join(row[0] for row in data)
            else:
                data = 'No data recorded'

            embed = create_embed(f'Total Messages Per User As Of {date}:', data, random_color()) 
            await interaction.response.send_message(embed=embed, ephemeral=False)
            
        else:
            embed = create_embed(f'The value, {date}, is not valid. Format the date as yyyy-mm-dd.', '', random_color()) 
            await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Total(bot))
