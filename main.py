from dotenv import load_dotenv
import os
import logging
from bot import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

if __name__ == "__main__": 
    bot = Bot(guild_ids=[int(os.getenv('GUILD_ID'))]  )
    bot.run(os.getenv('BOT_TOKEN'))