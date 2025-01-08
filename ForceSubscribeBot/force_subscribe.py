#force_subscribe.py
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from ForceSubscribeBot.admin_check import admin_check
from pyrogram.errors import UsernameInvalid, PeerIdInvalid, UserNotParticipant
from ForceSubscribeBot.database.chats_sql import get_force_chat, change_force_chat, get_only_owner

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(filters.text & filters.incoming & filters.command(["fsub", "forcesubscribe"]))
async def fsub(bot, msg: Message):
    chat_id = msg.chat.id
    bot_id = (await bot.get_me()).id
    success = await admin_check(bot, msg)
    
    if not success:
        return

    if len(msg.command) == 1:
        # Get and display the current force subscribe chat
        force_chat = await get_force_chat(chat_id)
        if force_chat:
            chat = await bot.get_chat(force_chat)
            mention = '@' + chat.username if chat.username else f"{chat.title} ({chat.id})"
            await msg.reply(f"**Current Force Subscribe Chat** is: {mention}\n\nCould be changed using `/forcesubscribe new_chat_id`")
        else:
            await msg.reply("No force subscribe chat set!\n\nIt could be set using `/forcesubscribe chat_id`")
    else:
        # Ensure that only the owner or creator can modify the Force Subscribe chat
        creator = True if (await bot.get_chat_member(chat_id, msg.from_user.id)).status == "creator" else False
        only_owner = await get_only_owner(chat_id)
        
        if only_owner and not creator:
            await msg.reply("Only the owner can change the Force Subscribe chat in this chat.")
            return

        to_be_chat = msg.command[1]

        # Try to add the new chat to the force subscribe list
        try:
            bot_chat_member = await bot.get_chat_member(to_be_chat, bot_id)
        except (UsernameInvalid, PeerIdInvalid) as e:
            logger.error(f"Error with provided chat: {to_be_chat}, {str(e)}")
            await msg.reply(
                "Unsuccessful :( \n\nPossible reasons could be: \n\n"
                "1) I haven't been added there. \n"
                "2) The provided chat_id/username is invalid. \n"
                "3) I have been demoted there. \n"
                "4) You have provided a link instead of a username/chat_id. \n\n"
                "Please re-check all three and try again! If the problem persists, try demoting and promoting again."
            )
            return
        except ValueError as e:
            logger.error(f"ValueError occurred: {str(e)}")
            await msg.reply(f"Seriously? \n\n{str(e)}")
            return
        except UserNotParticipant:
            await msg.reply(f"I haven't been added to {to_be_chat}. Please add me first.")
            return

        # Check if the bot is an administrator in the provided chat
        if bot_chat_member.status == "administrator":
            to_be_chat_id = (await bot.get_chat(to_be_chat)).id
            await change_force_chat(chat_id, to_be_chat_id)
            await msg.reply("Successfully updated the force subscribe chat. Now I'll mute people who haven't joined that chat. \n\nUse /settings to change settings.")
        else:
            await msg.reply("Please make me an admin in the provided chat and then try again!")
