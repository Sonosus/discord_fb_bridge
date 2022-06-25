import discord
import logging
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

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
async def post_image(image_location):
    # image storage endpoint
    image_url = 'https://graph.facebook.com/{}/photos'.format(PAGE_ID)
    # request payload
    img_payload = {
    'url': image_location,
    'access_token': FB_ACCESS_TOKEN
    }
    logging.info("Image source URL: " + str(img_payload["url"]))
    
    #Send the POST request
    r = requests.post(image_url, data=img_payload)
    logging.info("GET request sent with response" + r.text)
    return r

client = discord.Client()

@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    channel = message.channel
    author = message.author
    print(channel.id)
    if author == client.user:
        return
    
    if channel.id != 989976934672904212:
        logging.info("Message %s not in channel", message.id)
        return
    
    logging.info("Message posted in channel")
    if message.attachments:
        for a in message.attachments:
            logging.info("Attachment with URL " + a.url + "found.")
            if a.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".heif")):
                post = await post_image(a.url)
                if post.status_code == 200:
                    await message.reply("Posted to Facebook. See your post at https://facebook.com/" + str(PAGE_ID))
                else:
                    await message.reply("Unknown API error. Try again or contact staff.")
            else:
                await message.reply("Unrecognised file type. Supported image types are JPEG, PNG, GIF, WEBP, TIFF, HEIF. Please try again. Note that at this time video upload is not supported.")  
    else:
        logging.info("Message " + str(message.id) + " did not contain attachments.")
        await message.reply("That post did not contain any images, please try again.", mention_author=True)

client.run(DISCORD_TOKEN)