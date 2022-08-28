from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from api.users.endpoints.serializers import User, Login
from api.users.auth.utils import get_current_user
from api.users.utils.blacklist_tokens import is_token_blacklisted
from api.users.handlers.user_handler import (
    UserSignupHandler,
    UserLoginHandler,
    UserLogoutHandler,
)

# router object for handling api routes
router = APIRouter()


@router.post("/login", response_description="login a user")
def login(user_credential: Login):
    user_login = UserLoginHandler(user_credential).login_user()
    return user_login


@router.post("/logout", response_description="logout a user")
def logout(current_user: dict = Depends(get_current_user)):
    user_logout = UserLogoutHandler(current_user).logout_user()
    return user_logout


@router.get("/me", response_description="Get details of currently logged in user")
async def get_me(user: dict = Depends(get_current_user)):
    if is_token_blacklisted(user["token"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Login first"
        )
    return user


@router.post("/signup", response_model=User, response_description="logout a user")
def signup(user: User):
    new_user = UserSignupHandler(user).add_user_to_db()
    created_user = {"user": user.first_name, "status": "created"}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
