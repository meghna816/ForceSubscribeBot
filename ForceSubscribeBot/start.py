#start.py
from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Message
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
    try:
        user = await bot.get_me()
        mention = user["mention"]
        user_mention = msg.from_user.mention

        # Get user stats (for example, number of interactions with the bot)
        # Assuming you have a method to fetch user stats
        user_stats = await get_user_stats(msg.from_user.id)

        # Format start message with dynamic user stats
        start_message = Data.START.format(user_mention, mention, user_stats)

        # Custom buttons (Could be dynamic based on user preferences)
        buttons = [
            [InlineKeyboardButton("Get Help", callback_data="help"),
             InlineKeyboardButton("Settings", callback_data="settings")],
            [InlineKeyboardButton("Choose Language", callback_data="choose_language")]
        ]

        # Send personalized message with buttons
        await bot.send_message(
            msg.chat.id,
            start_message,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await msg.reply("Sorry, something went wrong. Please try again later.")

# Example function to simulate fetching user stats (can be expanded)
async def get_user_stats(user_id):
    # For demo purposes, we're just returning a dummy value
    # You can integrate this with your database to track the number of interactions
    return f"You have interacted with me {user_id % 100} times."
