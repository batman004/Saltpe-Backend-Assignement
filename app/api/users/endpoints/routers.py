from fastapi import APIRouter, Request, HTTPException
from api.users.handlers.user_handler import UserHandler
from api.users.endpoints.serializers import User

# router object for handling api routes
router = APIRouter()


@router.post("/login", response_description="login a user")
async def login(user: User):
    pass


@router.post("/logout", response_description="logout a user")
async def logout(user: User):
    pass


@router.post("/signup", response_description="logout a user")
async def signup(user: User):
    pass
