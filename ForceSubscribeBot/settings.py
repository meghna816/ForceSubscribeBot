#settings.py
from pyrogram import Client, filters
from ForceSubscribeBot.admin_check import admin_check
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ForceSubscribeBot.database.chats_sql import get_action, get_ignore_service, get_only_owner, chat_exists

@Client.on_message(filters.text & filters.incoming & filters.command("settings"))
async def settings(bot: Client, msg):
    # Ensure the user is an admin
    success = await admin_check(bot, msg)
    if not success:
        return

    chat_id = msg.chat.id

    # Check if the force subscribe chat is set
    if not await chat_exists(chat_id):
        await msg.reply("Please add a force subscribe chat using /fsub to use me.")
        return

    # Check if only the owner can change settings
    only_owner = await get_only_owner(chat_id)
    is_creator = (await bot.get_chat_member(chat_id, msg.from_user.id)).status == "creator"

    if only_owner and not is_creator:
        await msg.reply("Only the owner can change settings in this chat.")
        return

    # Generate the settings buttons
    buttons = await action_markup(chat_id)

    # Send the settings message
    await msg.reply(
        "**Settings** \n\n"
        "1) Choose an action for users who haven't joined the force subscribe chat. Defaults to Mute.\n"
        "2) Choose whether to ignore welcome messages. Defaults to On.\n"
        "3) Choose whether admins can change settings or only the owner can. Defaults to 'Allow Only Owner'.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def action_markup(chat_id):
    # Get current settings
    action = await get_action(chat_id)
    actions = {"warn": "Warn", "mute": "Mute", "kick": "Kick", "ban": "Ban"}
    action_buttons = {key: value + (" ✅" if action == key else "") for key, value in actions.items()}

    # Get ignore service status
    ignore_service = await get_ignore_service(chat_id)
    ignore_service_text = "Ignore Welcome Message: " + ("On" if ignore_service else "Off")
    ignore_service_data = "on" if ignore_service else "off"

    # Get only owner status
    only_owner = await get_only_owner(chat_id)
    only_owner_text = "Allow Only Owner" if only_owner else "Allow Admins Too"
    only_owner_data = "True" if only_owner else "False"

    # Define the buttons for actions and settings
    buttons = [
        [
            InlineKeyboardButton(action_buttons["warn"], callback_data=f"action+warn+{chat_id}"),
            InlineKeyboardButton(action_buttons["mute"], callback_data=f"action+mute+{chat_id}"),
            InlineKeyboardButton(action_buttons["kick"], callback_data=f"action+kick+{chat_id}"),
            InlineKeyboardButton(action_buttons["ban"], callback_data=f"action+ban+{chat_id}")
        ],
        [
            InlineKeyboardButton(ignore_service_text, callback_data=f"action+{ignore_service_data}+{chat_id}")
        ],
        [
            InlineKeyboardButton(only_owner_text, callback_data=f"action+{only_owner_data}+{chat_id}")
        ]
    ]
    return buttons
