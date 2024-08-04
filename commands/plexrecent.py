import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from plexapi.server import PlexServer
import os
from utils.helper import create_embed, random_color
from dotenv import load_dotenv 

load_dotenv()

plex_base_url = os.getenv('PLEX_BASE_URL')
plex_token = os.getenv('PLEX_TOKEN')
pub_plex_base_url = os.getenv('PUB_PLEX_BASE_URL')

class PlexRecent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="plexrecent", description="Get movies added in the last X days")
    @app_commands.describe(days="Number of days to look back")
    async def plexrecent(self, interaction: discord.Interaction, days: app_commands.Range[int, 0, 90]):
        await interaction.response.defer()
        try:
            plex = PlexServer(plex_base_url, plex_token)
            library = plex.library 

            recently_added_movies = []
            for movie in library.section('Movies').all():
                if movie.addedAt and movie.addedAt >= datetime.now() - timedelta(days=days):
                    recently_added_movies.append({
                        "title": movie.title,
                        "audience_rating": movie.audienceRating,
                        "added_at": movie.addedAt.date().strftime('%Y-%m-%d'),
                        "image": pub_plex_base_url + movie.thumb + "?X-Plex-Token=" + plex_token
                    })
           
            sorted_movies = sorted(recently_added_movies, key=lambda x: x['audience_rating'], reverse=True)

            if sorted_movies:
                top_movies = 3
                for movie in sorted_movies[0:top_movies]:  
                    text = f"**{movie['title']}**\n:popcorn: Rating: {movie['audience_rating']}\n:calendar: Added: {movie['added_at']}"
                    embed = create_embed(f'Top Plex Movie additions in the last {days} days:', text, random_color())
                    embed.set_image(url=movie['image'])
                    await interaction.followup.send(embed=embed) 
                
                if sorted_movies[top_movies+1:-1]:
                    formatted_movies = "\n\n".join(
                        f"**{movie['title']}**\n:popcorn: Rating: {movie['audience_rating']}\n:calendar: Added: {movie['added_at']}"
                        for movie in sorted_movies[top_movies+1:-1]
                    )
                    embed = create_embed(f'Other Plex Movie additions in the last {days} days:', formatted_movies, random_color())
                    await interaction.followup.send(embed=embed)
            else:
                embed = create_embed(f'No movies added in the last {days} days:', 'Try increasing the days requested.', random_color())
                await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error searching Plex movie library: {e}")
            embed = create_embed(f"Error occurred:", f"Error: {e}", discord.Color.red())
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PlexRecent(bot))
