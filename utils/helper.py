from datetime import datetime, timedelta
import pytz

def get_date_time(formatted=False):
    now = datetime.now()
    if formatted:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    return now 

def change_tz(datetime, hours):
    return (datetime + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    #2024-07-18 17:04:02