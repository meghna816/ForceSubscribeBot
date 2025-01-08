#users_sql.py
from sqlalchemy import Column, BIGINT, String
from . import BASE, SESSION
from sqlalchemy.exc import SQLAlchemyError


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    user_id = Column(BIGINT, primary_key=True)
    channels = Column(String, nullable=True)

    def __init__(self, user_id):
        self.user_id = user_id


# Create table only if it does not exist
Users.__table__.create(checkfirst=True)


# Helper function for managing queries with error handling
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


async def num_users():
    return await _execute_query(SESSION.query(Users).count())
