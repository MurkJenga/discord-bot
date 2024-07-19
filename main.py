from dotenv import load_dotenv
import os
from bot import Bot

load_dotenv()

if __name__ == "__main__":
    Jengar = Bot()
    Jengar.run(os.getenv('BOT_TOKEN'))
