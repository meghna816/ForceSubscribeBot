#must_join.py
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from Config import MUST_JOIN

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(~filters.edited & filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # If MUST_JOIN is not set, do nothing
        return

    # Try to check if the user is part of the required channel
    try:
        await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
    except UserNotParticipant:
        # If user is not a participant, send the invite link
        if MUST_JOIN.isalpha():
            link = f"https://t.me/{MUST_JOIN}"
        else:
            try:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            except Exception as e:
                logger.error(f"Error fetching chat info for {MUST_JOIN}: {e}")
                return  # If something goes wrong, just return

        try:
            await msg.reply(
                f"You must join [this channel]({link}) to use me. After joining, try again!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✨ Join Channel ✨", url=link)]
                ])
            )
            await msg.stop_propagation()  # Prevent further message processing
        except ChatWriteForbidden:
            logger.warning(f"Cannot send message to {msg.chat.id}, write access forbidden.")
    except ChatAdminRequired:
        logger.error(f"I'm not admin in the MUST_JOIN chat: {MUST_JOIN}")

