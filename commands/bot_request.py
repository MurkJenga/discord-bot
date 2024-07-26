import discord
from discord.ext import commands
from discord import app_commands
from utils.helper import create_embed, get_date_time, random_color
from utils.api_functions import send_json_request

class BotRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='botrequest', description='Make a feature request for the bot')
    @app_commands.describe(prompt='Request')
    async def botrequest(self, interaction: discord.Interaction, prompt: str):
        try:  
            data = {
                "type": 'bot',
                "request_text": prompt,
                "request_time": get_date_time(True)
                }
            send_json_request(data, 'request')
            embed = create_embed(f'Bot Request:', prompt, random_color())
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print('Error', e)
            embed = create_embed(f'This request did not work', prompt, discord.Color.red())
            await interaction.response.send_message(embed=embed) 

async def setup(bot):
    await bot.add_cog(BotRequest(bot))
