from datetime import datetime, timedelta
import discord

def get_date_time(formatted=False):
    now = datetime.now()
    if formatted:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    return now 

def change_tz(datetime, hours):
    return (datetime + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    #2024-07-18 17:04:02

def get_emoji_data(emoji):
            if isinstance(emoji, (discord.Emoji, discord.PartialEmoji)):
                return {
                    "name": emoji.name,
                    "id": str(emoji.id) if emoji.id else None
                }
            else:
                # Unicode emoji
                return {
                    "name": str(emoji),
                    "id": None
                }