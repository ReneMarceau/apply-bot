import discord
import feedparser
import asyncio
import html
from datetime import datetime, timedelta
from config import DISCORD_TOKEN, UPWORK_RSS_URL, KEYWORDS, DISCORD_CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Set to store IDs of jobs that have been sent
sent_jobs = set()

def clean_description(description):
    # Replace <br /> with newlines and strip out unnecessary parts
    clean_desc = description.split('<br /><br />')[0]  # Take only the relevant part before budget etc.
    clean_desc = clean_desc.replace('<br />', '\n')  # Replace <br /> with newlines
    return clean_desc

def parse_job_description(description):
    # Extract relevant parts from the description
    lines = description.split('<br />')
    job_details = {
        'budget': 'N/A',
        'posted_on': 'N/A',
        'category': 'N/A',
        'skills': 'N/A',
        'country': 'N/A',
        'apply_link': 'N/A'
    }
    
    for line in lines:
        line = html.unescape(line)  # Convert HTML entities to characters
        if '<b>Budget</b>' in line:
            job_details['budget'] = line.split('</b>: ')[1] if '</b>: ' in line else 'N/A'
        elif '<b>Posted On</b>' in line:
            job_details['posted_on'] = line.split('</b>: ')[1] if '</b>: ' in line else 'N/A'
        elif '<b>Category</b>' in line:
            job_details['category'] = line.split('</b>: ')[1] if '</b>: ' in line else 'N/A'
        elif '<b>Skills</b>' in line:
            job_details['skills'] = line.split('</b>: ')[1].strip() if '</b>: ' in line else 'N/A'
        elif '<b>Country</b>' in line:
            job_details['country'] = line.split('</b>: ')[1] if '</b>: ' in line else 'N/A'
        elif '<a href=' in line:
            job_details['apply_link'] = line.split('"')[1] if len(line.split('"')) > 1 else 'N/A'
    
    return job_details

async def check_new_jobs():
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    last_checked = datetime.now() - timedelta(minutes=10)
    
    while True:
        feed = feedparser.parse(UPWORK_RSS_URL)
        
        for entry in feed.entries:
            job_id = entry.id  # Unique ID for the job

            if job_id not in sent_jobs:
                published_time = datetime(*entry.published_parsed[:6])
                if published_time > last_checked:
                    if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower() for keyword in KEYWORDS):
                        clean_desc = clean_description(entry.description)
                        job_details = parse_job_description(entry.description)
                        
                        embed = discord.Embed(
                            title=entry.title,
                            url=entry.link,
                            description=clean_desc,
                            color=discord.Color.green()
                        )
                        embed.add_field(name="Category", value=job_details['category'], inline=True)
                        embed.add_field(name="Country", value=job_details['country'], inline=True)
                        embed.add_field(name="Budget", value=job_details['budget'], inline=True)
                        embed.add_field(name="Skills", value=job_details['skills'], inline=False)
                        embed.add_field(name="Apply", value=f"[Click to apply]({job_details['apply_link']})", inline=False)
                        
                        embed.set_footer(text=f"Published: {entry.published}")
                        
                        await channel.send(embed=embed)
                        sent_jobs.add(job_id)
        
        last_checked = datetime.now()
        await asyncio.sleep(300)  # Check every 5 minutes

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(check_new_jobs())

def run_bot():
    client.run(DISCORD_TOKEN)
