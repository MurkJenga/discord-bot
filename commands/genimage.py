import discord
from discord.ext import commands
from discord import app_commands
from utils.helper import generate_ai_image, create_embed, random_color, getimagai

class GenImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='genimage', description='Generage an image with AI')
    @app_commands.describe(prompt='Text Prompt')
    async def chatgpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer() 
        try: 
            embed = create_embed(f'Text Used To Generate Image:', prompt, random_color()) 
            embed.set_image(url=getimagai(prompt))
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print('Error', e)
            embed = create_embed(f'An error occurred while generating the image', 'Jengar will resolve issue later', discord.Color.red())
            await interaction.followup.send('An error occurred while generating the image.')

async def setup(bot):
    await bot.add_cog(GenImage(bot))     