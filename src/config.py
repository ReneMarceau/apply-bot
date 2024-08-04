import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
KEYWORDS = os.getenv("KEYWORDS").split(",")
UPWORK_RSS_URL = os.getenv("UPWORK_RSS_URL")
