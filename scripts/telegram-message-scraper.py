import os
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
MONGODB_URI = os.getenv("MONGODB_URI")

# Telegram client
client = TelegramClient("EthioMartScraperSession", API_ID, API_HASH)

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
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Channels to scrape
CHANNELS = [
    "@ZemenExpress",
    "@sinayelj",
    "@MerttEka",
    "@yebatochmregagroup",
    "@helloomarketethiopia",
    "@Leyueqa",
    "@kstoreaddis",
    "@Fashiontera"
]

def preprocess_text(text):
    """Clean and normalize Amharic messages."""
    if not text:
        return ""
    cleaned = text.replace("\n", " ").replace("፡", "").replace("\xa0", " ").strip()
    return cleaned

def split_metadata_and_content(structured_messages):
    metadata_records = []
    content_records = []

    for msg in structured_messages:
        metadata_records.append({
            "message_id": msg["message_id"],
            "channel": msg["channel"],
            "sender_id": msg["sender_id"],
            "timestamp": msg["timestamp"],
            "type": msg["type"],
            "has_media": msg["has_media"],
            "media_path": msg["media_path"],
            "media_downloaded": msg["media_downloaded"]
        })

        content_records.append({
            "message_id": msg["message_id"],
            "text": msg["text"],
            "cleaned_text": msg["cleaned_text"]
        })

    metadata_df = pd.DataFrame(metadata_records)
    content_df = pd.DataFrame(content_records)

    return metadata_df, content_df

async def scrape_channel_text_only(channel_username, limit_per_batch=200):
    """Scrape text-only messages for a given channel. Mark media-containing messages."""
    logger.info(f"Starting text-only scrape for {channel_username}")
    total_scraped = 0

    try:
        async for message in client.iter_messages(channel_username, limit=limit_per_batch):
            structured = {
                "channel": channel_username,
                "sender_id": message.sender_id,
                "timestamp": message.date,
                "message_id": message.id,
                "text": message.text or "",
                "cleaned_text": preprocess_text(message.text or ""),
                "has_media": isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)),
                "media_path": None,
                "media_downloaded": False,
                "type": "image/document" if message.media else "text"
            }

            try:
                collection.insert_one(structured)
                total_scraped += 1
            except Exception as e:
                logger.error(f"Failed to insert message {message.id} into MongoDB: {e}")

        logger.info(f"Finished {channel_username} | Total text messages scraped: {total_scraped}")
    except Exception as e:
        logger.error(f"Error scraping {channel_username}: {e}")

async def main():
    await client.start(PHONE_NUMBER)
    for channel in CHANNELS:
        await scrape_channel_text_only(channel)
    await client.disconnect()
    logger.info("✅ Text-only scraping complete for all channels.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Scraper interrupted by user.")
