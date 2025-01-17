#callbacks.py
import logging
from Data import Data
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from pyrogram.errors.exceptions import UserNotParticipant
from ForceSubscribeBot.database.chats_sql import (
    get_action,
    change_action,
    get_force_chats,  # Updated to handle list of IDs
    get_ignore_service,
    toggle_ignore_service,
    get_only_owner,
    toggle_only_owner
)
from ForceSubscribeBot.admin_check import admin_check
from ForceSubscribeBot.settings import action_markup

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    user_id = callback_query.from_user.id
    mention = user["mention"]
    query = callback_query.data.lower()

    try:
        if query.startswith("home"):
            if query == 'home':
                chat_id = callback_query.from_user.id
                message_id = callback_query.message.message_id
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=Data.START.format(callback_query.from_user.mention, mention),
                    reply_markup=InlineKeyboardMarkup(Data.buttons),
                )
        elif query == "about":
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.ABOUT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.home_buttons),
            )
        elif query == "help":
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="**Here's How to use me**\n" + Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.home_buttons),
            )
        elif query.startswith("action"):
            success = await admin_check(bot, callback_query.message, user_id, callback_query)
            if not success:
                return
            main = query.split("+")[1].lower()
            chat_id = int(query.split("+")[2])
            only_owner = await get_only_owner(chat_id)
            creator = True if (await bot.get_chat_member(chat_id, callback_query.from_user.id)).status == "creator" else False
            if only_owner and not creator:
                await callback_query.answer("Only owner can change settings in this chat.", show_alert=True)
                return
            if main in ["on", "off"]:
                current_bool = await get_ignore_service(chat_id)
                damn = True if main == "on" else False
                if current_bool != damn:
                    await toggle_ignore_service(chat_id, not current_bool)
                    action_message = "Now the service messages will not be checked!" if not current_bool else "Now the service messages will be checked too!"
                    await callback_query.answer(action_message, show_alert=True)
            elif main in ["true", "false"]:
                creator = True if (await bot.get_chat_member(chat_id, callback_query.from_user.id)).status == "creator" else False
                if not creator:
                    await callback_query.answer("This is a special setting and can only be changed by owner.", show_alert=True)
                    return
                current_bool = await get_only_owner(chat_id)
                damn = True if main == "true" else False
                if current_bool != damn:
                    await toggle_only_owner(chat_id, not current_bool)
                    action_message = "Now only owner can change fsub chat and settings!" if not current_bool else "Now admins can change fsub chat and settings!"
                    await callback_query.answer(action_message, show_alert=True)
            else:
                current_action = await get_action(chat_id)
                if main == current_action:
                    await callback_query.answer(f"{main.capitalize()} is already the action type.", show_alert=True)
                    return
                else:
                    await change_action(chat_id, main)

            buttons = await action_markup(chat_id)
            await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

        elif query.startswith("joined"):
            try:
                muted_user_id = int(query.split('+')[1])
            except IndexError:
                logger.warning("No user ID found in the 'joined' query.")
                return  # Early return if the user ID is missing in the query

            chat_id = callback_query.message.chat.id
            bot_id = (await bot.get_me()).id
            force_chats = await get_force_chats(chat_id)  # Get force chat IDs
            bot_chat_member = await bot.get_chat_member(chat_id, bot_id)

            # Loop through the force chats to check if user is in all of them
            for force_chat_id in force_chats:
                try:
                    await bot.get_chat_member(force_chat_id, muted_user_id)
                    # If user is a member, unmute them
                    await bot.unban_chat_member(chat_id, muted_user_id)
                    await callback_query.answer("Good Kid. You can start chatting properly in group now.", show_alert=True)
                    await callback_query.message.delete()
                except UserNotParticipant:
                    await callback_query.answer(f"Join the chat {force_chat_id} first then try!", show_alert=True)
                    return  # Return early if user is not a participant

    except Exception as e:
        logger.error(f"Error processing callback query: {e}")
        await callback_query.answer("An unexpected error occurred. Please try again later.", show_alert=True)
