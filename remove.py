# remove_and_sync_commands.py
import asyncio
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from bot import Bot   
load_dotenv()

async def remove_all_commands(bot: Bot):
    print("Removing all commands...")
    
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    print("Removed all global commands")

    if bot.guild_ids:
        for guild_id in bot.guild_ids:
            guild = discord.Object(id=guild_id)
            bot.tree.clear_commands(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"Removed all commands for guild {guild_id}")

async def sync_commands():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("No bot token found in .env file")

    dev_guild_ids = [969408146978275330]  
    bot = Bot(guild_ids=dev_guild_ids)
    
    try:
        await bot.login(bot_token)
        
        await remove_all_commands(bot)
        
        await bot.load_and_sync_commands()
        
        print("All commands have been removed and new commands synced successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(sync_commands())
