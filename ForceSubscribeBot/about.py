#about.py
import logging
from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, PeerIdInvalid


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# About Message
@Client.on_message(filters.private & filters.incoming & filters.command("about"))
async def about(bot, msg):
    try:
        # Send about message with inline buttons
        await bot.send_message(
            msg.chat.id,
            Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
        logger.info(f"Sent about message to {msg.chat.id}")
    except FloodWait as e:
        logger.warning(f"Rate limit exceeded, need to wait for {e.x} seconds.")
        await bot.send_message(msg.chat.id, f"Please wait {e.x} seconds before trying again.")
    except PeerIdInvalid as e:
        logger.error(f"Invalid chat ID: {e}")
        await bot.send_message(msg.chat.id, "An error occurred with your request.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        await bot.send_message(msg.chat.id, "Something went wrong. Please try again later.")

