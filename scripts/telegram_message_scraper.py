# src/telegram_scraper.py

import asyncio
from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime


class TelegramScraper:
    def __init__(self):
        load_dotenv('../.env')
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        self.phone = os.getenv('PHONE_NUMBER')
        self.client = None

    async def init_client(self):
        self.client = TelegramClient('scraping_session', self.api_id, self.api_hash)
        await self.client.start()

    async def scrape_channel(self, channel_username, writer, media_dir):
        entity = await self.client.get_entity(channel_username)
        channel_title = entity.title
        async for message in self.client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media:
                if hasattr(message.media, 'photo'):
                    filename = f"{channel_username}_{message.id}.jpg"
                    media_path = os.path.join(media_dir, filename)
                    await self.client.download_media(message.media, media_path)
                elif hasattr(message.media, 'document'):
                    filename = f"{channel_username}_{message.id}_{message.file.name}"
                    media_path = os.path.join(media_dir, filename)
                    await self.client.download_media(message.media, media_path)

            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

    async def scrape_channels(self, channels, output_file, media_dir):
        os.makedirs(media_dir, exist_ok=True)

        await self.init_client()
        async with self.client:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

                for channel in channels:
                    await self.scrape_channel(channel, writer, media_dir)
                    print(f"Scraped data from {channel}")

    def run_scraper(self, channels, output_file, media_dir):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scrape_channels(channels, output_file, media_dir))


if __name__ == "__main__":
    channels = [
        '@ZemenExpress', '@sinayelj', '@MerttEka', '@yebatochmregagroup',
        '@helloomarketethiopia', '@Leyueqa', '@kstoreaddis', '@Fashiontera'
    ]
    output_file = 'data/raw/telegram_data.csv'
    media_dir = 'data/raw/media'

    scraper = TelegramScraper()
    scraper.run_scraper(channels, output_file, media_dir)