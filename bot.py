import discord
from discord.ext import commands
import os
from utils.logging import logger, edit_logger
from utils.helper import get_date_time, change_tz

class Bot(commands.Bot):
    def __init__(self, command_prefix='!', command_directory='commands', **options):
        intents = discord.Intents.all()
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        self.command_directory = command_directory

    async def setup_hook(self):
        print("Loading commands...")
        await self.load_commands()
        print("Syncing commands...")
        await self.tree.sync()
        for command in self.tree.get_commands():
            print(f'Synced Command: {command.name}, Description: {command.description}')

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def load_commands(self):
        for filename in os.listdir(self.command_directory):
            if filename.endswith('.py') and filename != '__init__.py':
                extension = f'{self.command_directory}.{filename[:-3]}'
                try:
                    await self.load_extension(extension)
                except Exception as e:
                    print(f'Failed to load extension {extension}.')
                    print(e)

    async def on_message(self, message):
        msg = {
            "message_id": message.id,
            "author": message.author,
            "channel": message.channel,
            "content": message.content,
            "created_at": change_tz(message.created_at, -5),
            "edited_at": message.edited_at,
            "jump_url": message.jump_url,
            "mention_everyone": message.mention_everyone,
            "mentions": message.mentions
        }

        if 'peter' in message.content.lower() and 'mom' in message.content.lower():
            await message.channel.send('Penis')

        logger(msg["author"], 'created', msg["message_id"], msg["created_at"])

    async def on_message_delete(self, message):
        msg = {
            "message_id": message.id,
            "author": message.author,
            "channel": message.channel,
            "content": message.content,
            "created_at": change_tz(message.created_at, -5),
            "edited_at": message.edited_at,
            "jump_url": message.jump_url,
            "mention_everyone": message.mention_everyone,
            "mentions": message.mentions
        }

        logger(msg["author"], 'deleted', msg["message_id"], get_date_time(True))

    async def on_message_edit(self, before, after):
        edit_logger(before.author, before.id, get_date_time(True), before.content, after.content)

    async def on_reaction_add(self, reaction, user):
        logger(user, 'added reaction', reaction.message.id, get_date_time(True), reaction)

    async def on_reaction_remove(self, reaction, user):
        logger(user, 'removed reaction', reaction.message.id, get_date_time(True), reaction)
 
