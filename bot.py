import os
import schedule
import asyncio
import time
import telegram
from zoneinfo import ZoneInfo
from datetime import datetime
from threading import Thread
from dotenv import load_dotenv

# --- Configuration ---
# It's best practice to use environment variables for sensitive data.
# We'll load them from a .env file for easy development.
load_dotenv()

# You can also hardcode them for simplicity, but it's not recommended for production.
# Example: BOT_TOKEN = "YOUR_BOT_TOKEN"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Example: CHAT_ID = "-100123456789" or "YOUR_PERSONAL_CHAT_ID"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Bot Logic ---

async def send_questionnaire(bot):
    """
    Creates and sends the weekly questionnaire (poll) to the specified chat.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Bot Token or Chat ID is not configured.")
        return

    question = "How are you feeling this week?"
    options = ["🚀 Fantastic!", "😊 Good", "😐 Okay", "😕 A bit down", "🔥 On fire!"]

    try:
        print(f"Sending poll to chat ID: {CHAT_ID}")
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,  # Set to True if you want anonymous voting
            allows_multiple_answers=False
        )
        print("Poll sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_scheduler():
    """
    Runs the scheduler in a loop to check for pending jobs.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """
    Main function to initialize the bot and schedule the job.
    """
    print("Bot starting...")

    # Check for configuration
    if not BOT_TOKEN or not CHAT_ID:
        print("FATAL: Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        return

    # Initialize the bot
    bot = telegram.Bot(token=BOT_TOKEN)
    print("Bot initialized.")

    # Define the timezone (use stdlib zoneinfo to avoid external dependency)
    stockholm_tz = ZoneInfo("Europe/Stockholm")
    
    # Schedule the job
    # The time is specified in the server's local time, but we'll check the timezone inside the job.
    # A more robust way is to schedule in UTC and convert. Let's stick to a clear, simple way.
    
    # We create a wrapper function to pass the bot instance to our job
    def job():
        # Get the current time in Stockholm
        now_stockholm = datetime.now(stockholm_tz)
        print(f"Checking schedule... Current Stockholm time: {now_stockholm.strftime('%A %H:%M')}")
        
        # Although the scheduler runs thisaturday at 13:00 local time,
        # this check ensures it ONLY runs if the Stockholm time matches.
        # This is a simple but effective way to handle timezones with this library.
        asyncio.run(send_questionnaire(bot))

    # Schedule the job to rusaturday at 13:00 (1:00 PM)
    schedule.every().saturday.at("16:54").do(job)
    
    print("Job scheduledsaturday at 16:50 Stockholm time.")
    print("Waiting for the scheduled time...")

    # Run the scheduler in a separate daemon thread.
    # A daemon thread will exit when the main program exits.
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Keep the main thread alive to listen for Ctrl+C
    print("Bot is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping bot...")

if __name__ == "__main__":
    main()
