#id.py
import logging
from pyrogram import Client, filters

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(filters.text & filters.incoming & filters.command("id"))
async def id(_, msg):
    try:
        # Send the chat ID as a reply
        await msg.reply(f"Chat ID is : `{msg.chat.id}`", quote=True)
        logger.info(f"User {msg.from_user.id} requested their chat ID in chat {msg.chat.id}")
    except Exception as e:
        logger.error(f"Failed to fetch chat ID for {msg.chat.id}: {str(e)}")
        await msg.reply("Sorry, I encountered an issue while fetching the chat ID. Please try again later.")

