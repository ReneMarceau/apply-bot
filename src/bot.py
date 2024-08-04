import discord
import feedparser
import asyncio
from datetime import datetime, timedelta
from config import DISCORD_TOKEN, UPWORK_RSS_URL, KEYWORDS, DISCORD_CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def check_new_jobs():
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    last_checked = datetime.now() - timedelta(minutes=10)
    
    while True:
        feed = feedparser.parse(UPWORK_RSS_URL)
        
        for entry in feed.entries:
            published_time = datetime(*entry.published_parsed[:6])
            if published_time > last_checked:
                if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower() for keyword in KEYWORDS):
                    message = f"**{entry.title}**\n{entry.link}\n\n{entry.description[:200]}..."
                    await channel.send(message)
        
        last_checked = datetime.now()
        await asyncio.sleep(300)  # Check every 5 minutes

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(check_new_jobs())

def run_bot():
    client.run(DISCORD_TOKEN)
