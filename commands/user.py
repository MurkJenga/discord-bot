import discord
from discord.ext import commands
from discord import app_commands
from utils.api_functions import returnJsonResponse
from utils.helper import create_embed, random_color


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='user', description='Returns stats about a specific user')
    @app_commands.describe(user='Select the user you want to view the stats for.')
    async def user(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        data = returnJsonResponse(f'user/{user.id}')

        if len(data):
            data = {
                "user_id" : data[0]["user_id"],
                "username" : data[0]["username"],
                "join_date" : data[0]["joinDate"],
                "total_msgs" : format(data[0]["totalMsgs"], ','),
                "avg_words" : data[0]["averageWrds"],
                "last_msg" : data[0]["lastMsg"],
                "total_wrds" : format(int(data[0]["totalWrds"]), ','),
                "avg_per_day" : data[0]["avgPerDay"],
                "react_giv" : format(data[0]["reactGiv"], ','),
                "react_rec" : format(data[0]["reactRec"], ','),
                "top_react" : data[0]["topReact"]
            }
            embed = create_embed(f'{user}\'s stats', 'Moms Basement Stats Below', random_color()) 
            embed.add_field(name="Join Date", value= data["join_date"], inline=True)
            embed.add_field(name="Total Messages", value= data["total_msgs"], inline=True)
            embed.add_field(name="Avg Words Per Message", value= data["avg_words"], inline=True)
            embed.add_field(name="Last Message Sent", value= data["last_msg"], inline=True)
            embed.add_field(name="Total Words", value= data["total_wrds"], inline=True)
            embed.add_field(name="Average Messages Per Day", value= data["avg_per_day"], inline=True)
            embed.add_field(name="Emojis Given", value= data["react_giv"], inline=True)
            embed.add_field(name="Emojis Recieved", value= data["react_rec"], inline=True)
            embed.add_field(name="Top Emoji Used", value= data["top_react"], inline=True)  

            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            data = 'No data recorded'  
            embed = create_embed(f'No stats recorded for {user}', '', random_color()) 

            await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(User(bot))
