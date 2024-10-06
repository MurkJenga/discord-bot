import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import app_commands
from utils.helper import create_embed, random_color, get_date, parse_data

class Dropdown(discord.ui.Select):
    def __init__(self):
        self.article_data = self.get_articles()
        
        options = [
            discord.SelectOption(label=article["headline"]) 
            for article in self.article_data if article["headline"]
        ]
        
        super().__init__(placeholder='Choose an article', min_values=1, max_values=1, options=options)

    def get_articles(self):
        url = "https://www.morningbrew.com/daily/issues/latest"
        response = requests.get(url)
        html_content = response.text
        column_elements = None

        soup = BeautifulSoup(html_content, 'lxml')

        column_elements = soup.find_all('td', class_='card') if soup.find_all('td', class_='card') else soup.find_all('td', class_='column')
        
        articles = [parse_data(column) for column in column_elements]
        return articles
    
    def get_headlines(self):
        return [article["headline"] for article in self.article_data if article["headline"]]

    async def callback(self, interaction: discord.Interaction):
        selected_article = next((article for article in self.article_data if article.get("headline") == self.values[0]), None)

        if selected_article: 
            embed = discord.Embed(
                title=f'Morning Brew - {get_date()}',
                description='',
                color=random_color()
            )
            embed.add_field(name="Headline", value=selected_article["headline"], inline=False)
            embed.add_field(name="Story", value=selected_article["body"][:1024], inline=False)
            
            if selected_article.get("link"):
                embed.add_field(name="Read More Here", value=selected_article["link"], inline=False)
            
            if selected_article.get("image"):
                embed.set_image(url=selected_article["image"])

            await interaction.response.send_message(embed=embed)

            view = DropdownView()
            
            dropdown = view.children[0]
            headlines = dropdown.get_headlines()
            
            formatted_headlines = "\n".join(f"• {headline}" for headline in headlines)
            await interaction.followup.send(f"Here are today's headlines:\n{formatted_headlines}", view=view)
        else: 
            await interaction.response.send_message("Selected article not found.", ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class Brew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @app_commands.command(name='brew', description='Spill the morning brew for today') 
    async def brew(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            view = DropdownView() 
            
            dropdown = view.children[0]
            headlines = dropdown.get_headlines()
            
            formatted_headlines = "\n".join(f"• {headline}" for headline in headlines)
            
            await interaction.followup.send(f"Here are today's headlines:\n{formatted_headlines}", view=view)

        except Exception as e:
            print(f'Error: {e}')
            embed = create_embed(
                'Fetching the Morning Brew was not successful', 
                '', 
                discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Brew(bot))
