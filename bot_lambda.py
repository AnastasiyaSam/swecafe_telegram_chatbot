import os
import asyncio
import telegram

# --- Configuration ---
# In AWS Lambda, these will be set as environment variables in the function's configuration.
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_questionnaire_async():
    """
    Initializes the bot and sends the weekly questionnaire (poll).
    This async function is called by the Lambda handler.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables are not set.")
        return {"statusCode": 500, "body": "Configuration error: Missing environment variables."}

    bot = telegram.Bot(token=BOT_TOKEN)
    question = "Придете сегодня на кафе в 20.00 по Стокгольму?"
    options = ["Да", "Нет"]

    try:
        print(f"Sending poll to chat ID: {CHAT_ID}")
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        print("Poll sent successfully!")
        return {"statusCode": 200, "body": "Poll sent successfully."}
    except Exception as e:
        print(f"An error occurred: {e}")
        # It's useful to return the error in the body for debugging
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}

def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    This function is triggered by an event, such as from Amazon EventBridge (for scheduling).
    """
    print("Lambda function execution started.")
    # Lambda handlers are synchronous, so we use asyncio.run() to call our async logic.
    result = asyncio.run(send_questionnaire_async())
    print("Lambda function execution finished.")
    return result

# The block below is for local testing and is not executed by AWS Lambda.
if __name__ == "__main__":
    # To test this script locally, you must first set the environment variables.
    # In your terminal (on Windows):
    # set TELEGRAM_BOT_TOKEN=your_token
    # set TELEGRAM_CHAT_ID=your_chat_id
    # Then run: python bot.py
    print("Executing local test...")
    response = lambda_handler(None, None)
    print(f"Local test finished with response: {response}")