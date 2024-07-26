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
return_limit = 15

class PlexSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="plexsearch", description="Search for movie in Plex Library")
    @app_commands.describe(title="Number of days to look back")
    async def plexsearch(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        try:
            plex = PlexServer(plex_base_url, plex_token)
            library = plex.library 

            search_results = []
            for movie in library.section('Movies').all():
                if title.lower() in movie.title.lower():
                    search_results.append({
                        "title": movie.title,
                        "audience_rating": movie.audienceRating if movie.audienceRating is not None else 0,
                        "added_at": movie.addedAt.date().strftime('%Y-%m-%d'),
                        "image": pub_plex_base_url + movie.thumb + "?X-Plex-Token=" + plex_token
                    })  

            if search_results:
                sorted_movies = sorted(search_results, key=lambda x: x['audience_rating'], reverse=True)
                formatted_movies = "\n\n".join(
                        f"**{movie['title']}**\n:popcorn: Rating: {movie['audience_rating']}\n:calendar: Added: {movie['added_at']}"
                        for movie in sorted_movies[0:return_limit]
                    )
                embed = create_embed(f'Movies matching: {title}', formatted_movies, random_color())
            else:
                embed = create_embed(f'No movies matching: {title}', '', random_color())
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error searching Plex movie library: {e}")
            embed = create_embed(f"Error occurred:", f"Error: {e}", discord.Color.red())
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PlexSearch(bot))
