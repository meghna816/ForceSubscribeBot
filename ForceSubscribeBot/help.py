#help.py
import logging
from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Help Message
@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def _help(bot, msg):
    try:
        await bot.send_message(
            msg.chat.id,
            f"**Here's How to Use Me**\n{Data.HELP}",
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    except Exception as e:
        logger.error(f"Failed to send help message to {msg.chat.id}: {str(e)}")
        await msg.reply("Sorry, I encountered an issue while sending the help message. Please try again later.")
