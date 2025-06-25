from apscheduler.schedulers.blocking import BlockingScheduler
import os

# We assume text scraper and media fetcher are defined in other scripts
def run_text_scraper():
    os.system("python telegram_message_scraper.py")

def run_media_fetcher():
    os.system("python telegram-media-scraper.py")

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # 🕒 Run text scraper every hour
    scheduler.add_job(run_text_scraper, 'interval', minutes=60, id='telegram-message-scraper')

    # 🕒 Run media fetcher every 10 minutes
    scheduler.add_job(run_media_fetcher, 'interval', minutes=10, id='telegram-media-scraper')

    print("📅 Scheduler started. Press Ctrl+C to exit.")
    scheduler.start()
