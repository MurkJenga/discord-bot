from dotenv import load_dotenv
import discord
import os

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!') 

    async def on_message(self, message):
        msg = {
            "message_id": message.id,
            "author": message.author,
            "channel": message.channel,
            "content": message.content,
            "created_at": message.created_at,
            "edited_at": message.edited_at,
            "jump_url": message.jump_url,
            "mention_everyone": message.mention_everyone,
            "mentions": message.mentions
        }

        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        print(msg["author"], 'sent', msg["content"], 'at', msg["created_at"])

client = MyClient(intents=discord.Intents.all()) 
client.run(os.getenv('BOT_TOKEN'))
