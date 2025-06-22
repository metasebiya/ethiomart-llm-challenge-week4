import os
import asyncio
from datetime import datetime
from telethon import TelegramClient
from pymongo import MongoClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
MONGODB_URI = os.getenv("MONGODB_URI")

# Telegram client
client = TelegramClient("EthioMartMediaFetcherSession", API_ID, API_HASH)

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["ethio_ner"]
collection = db["telegram_messages"]

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/media_fetcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_media_path(channel, timestamp, message_id):
    date_folder = timestamp.strftime("%Y-%m-%d")
    channel_folder = channel.replace("@", "").replace(" ", "_")
    dir_path = os.path.join("downloads", date_folder, channel_folder)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, f"{message_id}_{datetime.utcnow().timestamp()}.jpg")

async def fetch_and_store_media():
    await client.start(PHONE_NUMBER)
    logger.info("Started media fetcher...")

    # Fetch messages needing media download
    messages = list(collection.find({"has_media": True, "media_downloaded": False}))
    logger.info(f"Found {len(messages)} messages to process...")

    for msg in messages:
        channel = msg["channel"]
        message_id = msg["message_id"]
        timestamp = msg["timestamp"]

        try:
            entity = await client.get_entity(channel)
            message = await client.get_messages(entity, ids=message_id)

            if not message or not message.media:
                logger.warning(f"No media found in message {message_id} from {channel}")
                continue

            media_path = create_media_path(channel, timestamp, message_id)
            downloaded = await client.download_media(message, media_path)

            if downloaded:
                # Update MongoDB record
                collection.update_one(
                    {"_id": msg["_id"]},
                    {"$set": {"media_path": downloaded, "media_downloaded": True}}
                )
                logger.info(f"Downloaded media for message {message_id} -> {downloaded}")
            else:
                logger.warning(f"Download failed for message {message_id}")

        except Exception as e:
            logger.error(f"Failed to fetch media for {channel} msg {message_id}: {e}")

    await client.disconnect()
    logger.info("✅ Media fetching completed.")

if __name__ == "__main__":
    try:
        asyncio.run(fetch_and_store_media())
    except KeyboardInterrupt:
        logger.info("⛔ Media fetcher interrupted by user.")
