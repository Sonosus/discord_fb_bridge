import discord

import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

# configure path to secrets file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")

async def post_image(image_location):
    # image storage endpoint
    image_url = 'https://graph.facebook.com/{}/photos'.format(PAGE_ID)
    # request payload
    img_payload = {
    'url': image_location,
    'access_token': FB_ACCESS_TOKEN
    }
    
    #Send the POST request
    r = requests.post(image_url, data=img_payload)
    print(r.text)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    channel = message.channel
    author = message.author
    print(channel.id)
    if author == client.user:
        return
    
    if channel.id != 989976934672904212:
        print("wrong channel")
        return
    
    print("yep!")
    for a in message.attachments:
        print(a)
        print(a.url)
        await post_image(a.url)

client.run(DISCORD_TOKEN)