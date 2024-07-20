import requests as r
from dotenv import load_dotenv
import os
import json

load_dotenv()

def send_json_request(data, endpoint):
    url = os.getenv('API_URL') + '/' + endpoint
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': os.getenv('API_KEY')
    }
    try:
        response = r.post(url, headers=headers, json=data) 
    
    except r.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None 