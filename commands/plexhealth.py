import discord, requests, os, logging, datetime
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from utils.helper import create_embed, random_color
from utils.api_functions import returnJsonResponse, send_json_request

load_dotenv()
utc = datetime.timezone.utc
time = [
    datetime.time(hour=1, tzinfo=utc),
    datetime.time(hour=13, tzinfo=utc)
]
logging.basicConfig(level=logging.INFO)

class PlexHealth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = [
            {
                'server': 'James\' Server',
                'heartbeat_id': 2875545,
                'user_id': 553337834090659899,
                'name': 'james'
            },
            {
                'server': 'Jake\' Server',
                'heartbeat_id': 2876528,
                'user_id': 284405732395188233,
                'name': 'jake'
            }
        ]
        self.status_check.start()

    @app_commands.command(name='plexhealth', description='Check if Plex is alive')
    async def plexhealth(self, interaction: discord.Interaction):
        await interaction.response.defer() 
        
        message_body = []
        
        for server in self.servers:
            response = await self.ping_betterstack(server)
            status = await self.get_plex_status(response)
            message = await self.build_message(server, status)
            message_body.append(message)

        embed = create_embed(
            "Plex Availability Status:",
            '\n\n'.join(message_body),
            random_color()
        )
        await interaction.edit_original_response(embed=embed) 

    async def ping_betterstack(self, server):
        try:
            url = f"https://uptime.betterstack.com/api/v2/monitors/{server['heartbeat_id']}"
            headers = {"Authorization": f"Bearer {os.getenv('BETTERSTACK_TOKEN')}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error pinging {server['server']}: {e}")
            return None 

    async def get_plex_status(self, response):
        if response and 'data' in response:
            return response['data']['attributes']['status']
        return 'down'  

    async def build_message(self, server, status):
        if status == 'up':
            return f"{server['server']} - 🟢 Healthy"
        else:
            return f"{server['server']} - 🔴 Down"
    
    @tasks.loop(hours=1)
    async def status_check(self):
        for server in self.servers:
            response = await self.ping_betterstack(server)
            status = await self.get_plex_status(response)
            message = await self.build_message(server, status)

            embed = create_embed(
                "Plex Availability Status:",
                message,
                random_color()
            )
            user = await self.bot.fetch_user(server['user_id'])  
            if status != 'up':
                try:
                    send_json_request(f"Updating {server['server']} status to down", f"command/plex/update/{server['name']}/1")
                    await user.send(embed=embed)  
                except discord.Forbidden:
                    logging.error(f"Could not send message to {user.name}")
            else: 
                previous_plex_status = returnJsonResponse(f"command/plex/status/{server['name']}")
                if previous_plex_status[0][0] == 1:
                    
                    status_embed = create_embed(
                        "Plex Restored:",
                        f"🟢  Plex availability for {server['server']} has been restored",
                        random_color()
                    )
                    send_json_request(f"Updating {server['server']} status to back up", f"command/plex/update/{server['name']}/0")
                    await user.send(embed=status_embed)
                    logging.info(f"Sent message to {server['name']} for Plex Server restoration")
                else:
                    logging.info(f'{server["server"]} - Server is up, not sending message')

async def setup(bot):
    await bot.add_cog(PlexHealth(bot))
