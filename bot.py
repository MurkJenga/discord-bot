import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from utils.logging import logger, edit_logger
from utils.helper import get_date_time, change_tz, get_emoji_data
from utils.api_functions import send_json_request

load_dotenv()

class Bot(commands.Bot):
    def __init__(self, command_prefix='!', command_directory='commands', guild_ids=None, **options):
        intents = discord.Intents.all()
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        self.command_directory = command_directory
        self.guild_ids = [int(os.getenv('GUILD_ID'))]   

    async def setup_hook(self):
        await self.load_and_sync_commands()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def load_and_sync_commands(self):
        print("Loading commands...")
        for filename in os.listdir(self.command_directory):
            if filename.endswith('.py') and filename != '__init__.py':
                extension = f'{self.command_directory}.{filename[:-3]}'
                try:
                    await self.load_extension(extension)
                    print(f'Loaded extension: {extension}')
                    cog = self.get_cog(filename[:-3].capitalize())
                    if cog:
                        for command in cog.get_app_commands():
                            print(f'  - Loaded command: {command.name}')
                except Exception as e:
                    print(f'Failed to load extension {extension}.')
                    print(f'Error: {e}')

        print("Syncing commands...")
        if self.guild_ids:
            for guild_id in self.guild_ids:
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                print(f"Synced commands for guild {guild_id}")
        else:
            await self.tree.sync()
        print("Commands synced!")

    async def on_message(self, message):  
        msg = {
            "channelId": str(message.channel.id),
            "guildId": str(message.guild.id),
            "messageId": str(message.id),
            "createdTime": change_tz(message.created_at, -5),
            "content": message.content,
            "ogContent": message.content,
            "authorId": str(message.author.id),
            #"jump_url": message.jump_url,
            #"mention_everyone": message.mention_everyone,
            #"mentions": message.mentions
        } 
                             
        if 'peter' in message.content.lower() and 'mom' in message.content.lower():
            await message.add_reaction(os.getenv('PETERS_MOM')) 

        send_json_request(msg, 'message/insertmessage') 
        logger(message.author, 'created', msg["messageId"], msg["createdTime"])  

    async def on_message_delete(self, message):
        msg = {
            "messageId": str(message.id)
        }

        send_json_request(msg, 'message/deletemessage')
        logger(message.author, 'deleted', msg["messageId"], get_date_time(True))

    async def on_message_edit(self, before, after):
        edit_logger(before.author, before.id, get_date_time(True), before.content, after.content)
        msg = {
            "updated_time": get_date_time(True),
            "content": after.content, 
		    "messageId": str(after.id)
        }
        send_json_request(msg, 'message/updatemessage') 

    async def on_reaction_add(self, reaction, user):  
        emoji_data = get_emoji_data(reaction.emoji)
        msg = {
            "userId": str(user.id),
            "messageId": str(reaction.message.id),
            "emojiName": emoji_data["name"],
            "emojiId": emoji_data["id"],
            "channelId": str(reaction.message.channel.id),
            "guildId": str(reaction.message.guild.id),
            "updateTIme": get_date_time(True)
        } 

        send_json_request(msg, 'emoji/insertemoji') 
        logger(user, 'added reaction', reaction.message.id, get_date_time(True), reaction)

    async def on_reaction_remove(self, reaction, user):
        emoji_data = get_emoji_data(reaction.emoji)
        msg = {
            "updateTIme": get_date_time(True),
            "messageId": str(reaction.message.id),
            "userId": str(user.id),
            "emojiName": emoji_data["name"]
        } 

        send_json_request(msg, 'emoji/updateemoji') 
        logger(user, 'removed reaction', reaction.message.id, get_date_time(True), reaction)  