from fastapi_users.db import SQLAlchemyUserDatabase
#from backend_app.services.data_access_layer.database_connection import database
from backend_app.services.auth.models.user_model import UserTable, UserDB
from backend_app.services.data_access_layer.database_connection import async_session_maker

async def get_user_db():
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(session, UserTable, UserDB)
