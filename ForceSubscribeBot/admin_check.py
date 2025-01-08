#admin_check.py
import logging
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, PeerIdInvalid
from ForceSubscribeBot.database.chats_sql import get_force_chats

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def admin_check(bot, msg, user_id=None, callback_query=None):
    if not user_id:
        user_id = msg.from_user.id
    
    bot_id = (await bot.get_me()).id
    
    # Ensure the command is used only in groups or supergroups
    if msg.chat.type not in ["supergroup", "group"]:
        await msg.reply("This command can only be used in Groups!", quote=True)
        logger.warning(f"User {user_id} tried to use the command in a non-group chat {msg.chat.id}.")
        return False
    
    try:
        # Get the member status for the bot and user
        chat_member = await msg.chat.get_member(user_id)
        bot_chat_member = await msg.chat.get_member(bot_id)
        
        # Check if bot is an admin in the chat
        if bot_chat_member.status != "administrator":
            text = "Please make me an admin and then try again!"
            logger.warning(f"Bot is not an admin in chat {msg.chat.id}.")
            if callback_query:
                await callback_query.answer(text, show_alert=True)
            else:
                await msg.reply(text)
            return False
        
        # Check if the user is an admin or the creator
        if chat_member.status not in ("creator", "administrator"):
            text = "This command is only for admins!"
            logger.warning(f"User {user_id} is not an admin or creator in chat {msg.chat.id}.")
            if callback_query:
                await callback_query.answer(text, show_alert=True)
            else:
                await msg.reply(text)
            return False
        
        # Get force chats for the current chat
        force_chats = await get_force_chats(msg.chat.id)
        
        # Check if the user is part of the force subscribe chat (using chat ID)
        for force_chat_id in force_chats:
            try:
                # Check if user is a participant in the force chat
                await bot.get_chat_member(force_chat_id, user_id)
            except UserNotParticipant:
                logger.error(f"User {user_id} is not a participant in the forced chat {force_chat_id}.")
                await msg.reply(f"You need to join the required group or channel to use this command.")
                return False

        # If everything is fine, return True
        logger.info(f"User {user_id} has admin rights and joined necessary groups/chats in chat {msg.chat.id}.")
        return True

    except UserNotParticipant:
        logger.error(f"User {user_id} is not a member of the chat {msg.chat.id}.")
        await msg.reply("You need to join the group to use this command.")
        return False
    except ChatAdminRequired:
        logger.error(f"Bot lacks admin rights in chat {msg.chat.id}.")
        await msg.reply("I need to be an admin in the group to perform this action.")
        return False
    except PeerIdInvalid:
        logger.error(f"Invalid user or group chat ID in message {msg.chat.id}.")
        await msg.reply("There was an issue with retrieving chat or user information.")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        await msg.reply("Something went wrong. Please try again later.")
        return False
