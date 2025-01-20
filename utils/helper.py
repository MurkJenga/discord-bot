from datetime import datetime, timedelta
import discord, openai, os, random, requests, json
from dotenv import load_dotenv 

load_dotenv()

def get_date_time(formatted=False):
    now = datetime.now()
    if formatted:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    return now 

def get_date(): 
    return datetime.today().strftime('%Y-%m-%d')

def change_tz(datetime, hours):
    return (datetime + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")

def get_emoji_data(emoji):
            if isinstance(emoji, (discord.Emoji, discord.PartialEmoji)):
                return {
                    "name": emoji.name,
                    "id": str(emoji.id) if emoji.id else None
                }
            else:
                return {
                    "name": str(emoji),
                    "id": None
                }      

def generate_chat_completion(prompt):
    openai.api_key = os.getenv('CHATGPT_KEY')
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',   
        messages=
        [
            {
                "role": "user", 
                "content": prompt
                }
        ],
        max_tokens=2000
    )
    return response.choices[0].message['content'].strip()

def getimagai(prompt):
     
    url = 'https://api.getimg.ai/v1/essential-v2/text-to-image'
    token = os.getenv('GETIMG_KEY')
    headers = {    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'}
    data = {
        "prompt": prompt,
        "response_format": "url"
        }

    response = requests.post(url, headers=headers, data=json.dumps(data)) 
    json_response = response.json() 
    return json_response['url'] 

def generate_chat_completion(prompt):
    openai.api_key = os.getenv('CHATGPT_KEY')
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',   
        messages=
        [
            {
                "role": "user", 
                "content": prompt
                }
        ],
        max_tokens=2000
    )
    return response.choices[0].message['content'].strip()

def generate_ai_image(prompt):
    openai.api_key = os.getenv('CHATGPT_KEY')
    response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
    return response['data'][0]['url']

def create_embed(title, description, color):
    return discord.Embed(title=title, description=description, color=color)

def random_color():
    color_1, color_2, color_3 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    color = discord.Color.from_rgb(color_1, color_2, color_3) 
    return color

def mom_reply():
     random_replies = [
        'Milk, milk, lemonade, \'round the corner fudge is made', 
        'She gave me a rimjob', 
        'Now both of them can call me \'daddy\'', 
        'I be destroying her ass', 
        'I bang her harder than a screen door in a hurricane', 
        'She know who really gives it to her good', 
        'Best door mat I\'ve ever found on the side of the road', 
        'I\'ve been considering a better model lately', 
        'Should be illegal for ass to be that easy',
        'I fucked her like Heath Ledger fucked Jake Gyllenhaal in Brokeback Mountain.',
        'I took that hobbit to Isengard.',
        'You\'d be surprised by how tight that pussy is after 6 kids and 50 years of making love to Guy.',
        'She is so wise in the bedroom',
        'She massaged my prostate',
        'I wore a Peter mask to make it extra weird. She most appreciated the nose.',
        'She was so reassuring and comforting when I ejaculated prematurely.',
        'We 69\'d in Peter\'s old bedroom.',
        'She roared like a lioness in heat.',
        'I put two starbursts up her hole and fished them out again with my tongue.'
     ]
     reply = random.choice(random_replies)

     return reply

def parse_data(column):
    article = {
        'headline': '', 
        'body': [],
        'link': '',
        'image': ''
    }
    
    headline = column.select_one('h1:not([class*="sponsored"])')
    if headline:
        article['headline'] = headline.get_text(strip=True) 
    
    article['body'] = '\n\n'.join([p.get_text(strip=True) for p in column.find_all('p')])
    
    first_link = column.find('a')
    if first_link and 'href' in first_link.attrs and first_link['href'] != '#': 
        article['link'] = first_link['href']
    
    image = column.find('img')
    if image and 'src' in image.attrs:
        article['image'] = image['src']
    
    return article