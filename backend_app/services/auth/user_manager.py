from fastapi_users.manager import BaseUserManager, UserManagerDependency
from backend_app.services.auth.models.user_model import UserDB
from backend_app.services.auth.user_database import get_user_db
from fastapi import Depends

class UserManager(BaseUserManager[UserDB, int]):
    user_db_model = UserDB

    async def on_after_register(self, user: UserDB, request=None):
        print(f"User {user.id} has registered.")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)