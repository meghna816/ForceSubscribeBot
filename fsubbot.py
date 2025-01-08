#fsubbot.py
import Config
import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


# Improved Logging Configuration
logging.basicConfig(
    level=logging.INFO,  # Changed to INFO for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Initialize the Client (App)
app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="ForceSubscribeBot"),
)

# Run Bot
if __name__ == "__main__":
    try:
        app.start()
        uname = app.get_me().username
        logging.info(f"@{uname} Started Successfully!")
    except (ApiIdInvalid, ApiIdPublishedFlood) as e:
        logging.error(f"API ID/API HASH error: {e}")
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid as e:
        logging.error(f"Access Token error: {e}")
        raise Exception("Your BOT_TOKEN is not valid.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise Exception(f"An unexpected error occurred: {e}")

    try:
        # Keeps the bot running until manually stopped
        logging.info("Bot is running... Waiting for new updates.")
        idle()
    finally:
        app.stop()
        logging.info("Bot stopped. Alvida!")

