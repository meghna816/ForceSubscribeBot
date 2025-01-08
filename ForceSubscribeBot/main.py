#main.py
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ChatPermissions
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from ForceSubscribeBot.database.chats_sql import get_force_chat, get_action, get_ignore_service
import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(filters.group, group=-1)
async def main(bot: Client, msg: Message):
    if not msg.from_user or msg.from_user.id in Config.DEVS:
        return

    user_id = msg.from_user.id
    chat_id = msg.chat.id
    force_chat = await get_force_chat(chat_id)
    ignore_service = await get_ignore_service(chat_id)

    # If service message and ignore_service is True, ignore it
    if ignore_service and msg.service:
        return

    # If no force chat is set, ignore the message
    if not force_chat:
        return

    # Check if the user is a participant in the force chat
    try:
        await bot.get_chat_member(force_chat, user_id)
    except UserNotParticipant:
        # If not a participant, take action
        chat_member = await msg.chat.get_member(user_id)

        if chat_member.status in ("creator", "administrator"):
            return  # Admins or creator can bypass this check

        # Fetch the force chat details
        chat = await bot.get_chat(force_chat)
        mention = '@' + chat.username if chat.username else f"[{chat.title}]({chat.invite_link})"
        link = chat.invite_link

        try:
            # Fetch the action to take (kick, ban, mute)
            action = await get_action(chat_id)
            buttons = [[InlineKeyboardButton("✨ Join This Chat ✨", url=link)]]

            if action == 'kick':
                await msg.chat.kick_member(user_id)
                await msg.chat.unban_member(user_id)
                await msg.reply("Kicked member because not joined Force Subscribe Chat")
                return
            elif action == 'ban':
                await msg.chat.kick_member(user_id)
                await msg.reply("Banned member because not joined Force Subscribe Chat")
                return
            elif action == 'mute':
                await msg.chat.restrict_member(user_id, ChatPermissions(can_send_messages=False))
                buttons.append([InlineKeyboardButton("Unmute Me", callback_data=f"joined+{msg.from_user.id}")])

            await msg.reply(
                f"You must join {mention} to chat here.",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            await msg.stop_propagation()  # Stop further message processing
        except ChatWriteForbidden:
            logger.warning(f"Unable to send message in chat {chat_id}, chat write is forbidden.")
        except Exception as e:
            logger.error(f"Error while processing force subscribe for user {user_id}: {e}")

    except ChatAdminRequired:
        # If bot doesn't have admin rights in the force chat, inform the user
        await msg.reply(f"I have been demoted in `{force_chat}` (force subscribe chat)!")

