#bot_users.py
import logging
from ForceSubscribeBot.database.users_sql import Users, num_users
from ForceSubscribeBot.database.chats_sql import num_chats
from ForceSubscribeBot.database import SESSION
from pyrogram import Client, filters
from pyrogram.types import Message
from sqlalchemy.exc import SQLAlchemyError


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User SQL Handler
@Client.on_message(~filters.edited & ~filters.service, group=1)
async def users_sql(_, msg: Message):
    if msg.from_user:
        try:
            # Checking if the user is already in the database
            q = SESSION.query(Users).get(int(msg.from_user.id))
            if not q:
                # If the user is not in the database, add them
                SESSION.add(Users(msg.from_user.id))
                SESSION.commit()
                logger.info(f"New user added: {msg.from_user.id}")
            else:
                logger.info(f"User {msg.from_user.id} already exists in the database.")
            SESSION.close()
        except SQLAlchemyError as e:
            logger.error(f"Database error while processing user {msg.from_user.id}: {e}")
            await msg.reply("An error occurred while processing your information. Please try again later.")
            SESSION.rollback()  # Ensure the session is not left in an inconsistent state
        except Exception as e:
            logger.error(f"Unexpected error while processing user {msg.from_user.id}: {e}")
            await msg.reply("Something went wrong. Please try again later.")


# Stats Command Handler
@Client.on_message(filters.user(1946995626) & ~filters.edited & filters.command("stats"))
async def _stats(_, msg: Message):
    try:
        # Fetching user and chat stats
        users = await num_users()
        chats = await num_chats()
        await msg.reply(f"Total Users: {users} \n\nTotal Chats: {chats}", quote=True)
        logger.info(f"Stats requested: Total Users - {users}, Total Chats - {chats}")
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        await msg.reply("An error occurred while fetching stats. Please try again later.")
