# ForceSubscribeBot/request_join/request_join.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ForceSubscribeBot.database.chats_sql import get_must_join, get_action
from ForceSubscribeBot.admin_check import admin_check

@Client.on_message(filters.private & filters.command("requestjoin"))
async def request_join(bot, msg):
    # Ensure the user is an admin
    success = await admin_check(bot, msg)
    if not success:
        return

    chat_id = msg.chat.id
    must_join_chats = await get_must_join(chat_id)

    if not must_join_chats:
        await msg.reply("No force subscribe chats configured. Use /fsub to set them.")
        return

    # Send the user the list of must-join channels/groups
    must_join_text = "\n".join([f"@{chat}" for chat in must_join_chats])
    await msg.reply(f"The following channels/groups are required for users to join before they can interact:\n{must_join_text}")

    # Inline buttons to guide users
    buttons = [
        [InlineKeyboardButton("View Settings", callback_data="settings")]
    ]

    await msg.reply(
        "Click the button below to manage settings or add/remove required chats.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
