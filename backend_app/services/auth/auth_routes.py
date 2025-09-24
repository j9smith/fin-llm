from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from backend_app.services.auth.auth import auth_backend
from backend_app.services.auth.user_manager import get_user_manager
from backend_app.services.auth.models.user_model import UserRead, UserCreate, UserUpdate, UserDB

fastapi_users = FastAPIUsers[UserDB, int](
    get_user_manager,
    [auth_backend],
)

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)