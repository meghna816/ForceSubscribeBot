#chats_sql.py
from sqlalchemy import Column, BigInteger, String, Boolean
from . import BASE, SESSION
from sqlalchemy.exc import SQLAlchemyError


class Chats(BASE):
    __tablename__ = "chats"
    __table_args__ = {'extend_existing': True}
    
    channel_id = Column(BigInteger, primary_key=True)
    force_chat = Column(BigInteger)
    action = Column(String)
    ignore_service = Column(Boolean, default=True)
    only_owner = Column(Boolean, default=True)

    def __init__(self, channel_id, force_chat, action='mute', ignore_service=True, only_owner=True):
        self.channel_id = channel_id
        self.force_chat = force_chat
        self.action = action
        self.ignore_service = ignore_service
        self.only_owner = only_owner


# Create table only if it does not exist
Chats.__table__.create(checkfirst=True)


async def _execute_query(query):
    try:
        result = await query
        SESSION.commit()
        return result
    except SQLAlchemyError as e:
        print(f"Error during query execution: {str(e)}")
        SESSION.rollback()
        return None
    finally:
        SESSION.remove()


async def num_chats():
    return await _execute_query(SESSION.query(Chats).count())


async def get_force_chat(chat_id):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        return chat.force_chat
    return None


async def change_force_chat(chat_id, force_chat):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        chat.force_chat = force_chat
    else:
        SESSION.add(Chats(channel_id=chat_id, force_chat=force_chat))
    await _execute_query(SESSION.commit())


async def get_action(chat_id):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        return chat.action
    return None


async def change_action(chat_id, action):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        chat.action = action
    else:
        SESSION.add(Chats(channel_id=chat_id, action=action))
    await _execute_query(SESSION.commit())


async def get_ignore_service(chat_id):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        return chat.ignore_service
    return False


async def toggle_ignore_service(chat_id, value):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        chat.ignore_service = value
        await _execute_query(SESSION.commit())
        return True
    return False


async def get_only_owner(chat_id):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        return chat.only_owner
    return False


async def toggle_only_owner(chat_id, value):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    if chat:
        chat.only_owner = value
        await _execute_query(SESSION.commit())
        return True
    return False


async def chat_exists(chat_id):
    chat = await _execute_query(SESSION.query(Chats).filter_by(channel_id=chat_id).first())
    return chat is not None
