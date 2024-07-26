import discord
from discord.ext import commands
from discord import app_commands
from utils.helper import generate_chat_completion, create_embed, random_color

class ChatGpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='chatgpt', description='Say something to Chat GPT')
    @app_commands.describe(prompt='Say Something')
    async def chatgpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()  # Defer the response
        try:  
            #embed = discord.Embed(title=f'ChatGPT was asked: {prompt}', description=generate_chat_completion(prompt) , color=0x00ff00)
            embed = create_embed(f'ChatGPT was asked: {prompt}', generate_chat_completion(prompt), random_color())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print('Error', e)
            embed = create_embed(f'Error occured:', f'Question asked: {prompt}', discord.Color.red())
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ChatGpt(bot))
