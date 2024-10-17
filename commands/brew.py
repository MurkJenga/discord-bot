import requests, datetime, os, discord
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord import app_commands
from utils.helper import create_embed, random_color, get_date, parse_data
from dotenv import load_dotenv

load_dotenv()

utc = datetime.timezone.utc
time = datetime.time(hour=13, minute=0, tzinfo=utc)

class Brew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedule_send.start()

    def get_articles(self):
        """Fetches the latest articles on-demand without retention."""
        url = "https://www.morningbrew.com/daily/issues/latest"
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'lxml')
        column_elements = soup.find_all('td', class_='card') or soup.find_all('td', class_='column')

        articles = [parse_data(column) for column in column_elements]
        return articles

    def get_headlines(self):
        """Fetch the headlines from the latest articles without caching."""
        articles = self.get_articles()
        headlines = [article["headline"] for article in articles if article.get("headline")]
        return "\n".join(f"• {headline}" for headline in headlines)

    @app_commands.command(name='brew', description='Spill the morning brew for today')
    async def brew(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            # Fetch and format the article headlines without retention
            headlines = self.get_headlines()

            # Create the dropdown view and send an embed
            view = DropdownView(self)
            embed = create_embed(f'Here are today\'s headlines: - {get_date()}', headlines, random_color())
            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            print(f'Error: {e}')
            embed = create_embed('Fetching the Morning Brew was not successful', '', discord.Color.red())
            await interaction.followup.send(embed=embed)

    def cog_unload(self):
        self.schedule_send.cancel()

    @tasks.loop(time=time)
    async def schedule_send(self):
        """Scheduled task to send the daily headlines to a specific channel."""
        try:
            channel_id = int(os.getenv('DAILY_NEWS_CHANNEL'))
            channel = self.bot.get_channel(channel_id)

            if channel:
                headlines = self.get_headlines()
                embed = create_embed(f'Headlines of The Day - {get_date()}', headlines, random_color())
                await channel.send(embed=embed)
            else:
                print("Channel not found")
        except Exception as e:
            print(f"Error in schedule_send: {e}")

class Dropdown(discord.ui.Select):
    def __init__(self, brew_cog):
        self.brew_cog = brew_cog
        article_data = self.brew_cog.get_articles()

        options = [
            discord.SelectOption(label=article["headline"])
            for article in article_data if article.get("headline")
        ]

        super().__init__(placeholder='Choose an article', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        article_data = self.brew_cog.get_articles()  # Fetch fresh data each time
        selected_article = next((article for article in article_data if article.get("headline") == self.values[0]), None)

        if selected_article:
            embed = discord.Embed(title=f'Morning Brew - {get_date()}', color=random_color())
            embed.add_field(name="Headline", value=selected_article["headline"], inline=False)
            embed.add_field(name="Story", value=selected_article["body"][:1024], inline=False)

            if selected_article.get("link"):
                embed.add_field(name="Read More Here", value=selected_article["link"], inline=False)

            if selected_article.get("image"):
                embed.set_image(url=selected_article["image"])

            await interaction.response.send_message(embed=embed)

class DropdownView(discord.ui.View):
    def __init__(self, brew_cog):
        super().__init__()
        self.add_item(Dropdown(brew_cog))

async def setup(bot):
    await bot.add_cog(Brew(bot))
