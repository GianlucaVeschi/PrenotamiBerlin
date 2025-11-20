#!/usr/bin/env python3
"""
Scheduler to run the Prenotami bot at specific times
Runs the bot every day at 7:00 AM (when new slots are released)
"""

import schedule
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from prenotami_bot import PrenotamiBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_bot_job():
    """Job to run the bot"""
    logger.info("="*70)
    logger.info(f"Scheduled job triggered at {datetime.now()}")
    logger.info("="*70)
    
    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    if not email or not password:
        logger.error("Missing credentials. Please check .env file")
        return
    
    try:
        bot = PrenotamiBot(email=email, password=password, headless=False)
        bot.run()
    except Exception as e:
        logger.error(f"Error running bot: {e}")


def main():
    """Main scheduler loop"""
    logger.info("="*70)
    logger.info("Prenotami Bot Scheduler Started")
    logger.info("="*70)
    logger.info("The bot will run every day at 7:00 AM")
    logger.info("Press Ctrl+C to stop the scheduler")
    logger.info("="*70)
    
    # Schedule the job at 7:00 AM every day
    schedule.every().day.at("07:00").do(run_bot_job)
    
    # Optional: Add additional time slots for backup attempts
    # Uncomment these lines if you want to try multiple times per day
    # schedule.every().day.at("07:05").do(run_bot_job)
    # schedule.every().day.at("07:10").do(run_bot_job)
    
    # Run once immediately for testing (comment out if you don't want this)
    logger.info("Running bot once immediately for testing...")
    run_bot_job()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user")


if __name__ == "__main__":
    main()

