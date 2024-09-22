import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import app_commands
from utils.helper import create_embed, random_color, get_date, parse_data

class Brew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='brew', description='Spill the morning brew for today') 
    async def brew(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:  
            url = "https://www.morningbrew.com/daily/issues/latest"
            response = requests.get(url)
            html_content = response.text

            soup = BeautifulSoup(html_content, 'lxml')  

            column_elements = soup.find_all('td', class_='column')  

            articles = [parse_data(column) for column in column_elements]

            for article in articles:
                if article['headline']:
                    print("\n---\n")
                    print(article)
            
                if article['headline']: 
                    embed = discord.Embed(title=f'Morning Brew - {get_date()}', description='', color=random_color())
                    embed.add_field(name="Headline", value= article["headline"], inline=False)
                    embed.add_field(name="Story", value= article["body"][:1024], inline=False) 
                    if article["link"]:
                        embed.add_field(name="Read More Here", value= article["link"], inline=False) 
                    embed.set_image(url=article['image'])

                    await interaction.followup.send(embed=embed)  

        except Exception as e:
            print('Error', e)
            embed = create_embed(f'Fetching the Morning Brew was not successful', '', discord.Color.red())
            await interaction.followup.send(embed=embed) 

async def setup(bot):
    await bot.add_cog(Brew(bot))
