from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from api.users.endpoints.serializers import User, Login
from api.users.endpoints.models import User as UserModel
from api.users.auth.hashing import Hash
from api.users.auth.jwt import create_access_token, create_refresh_token
from api.users.auth.utils import get_current_user
from api.users.handlers.user_handler import UserSignupHandler

# router object for handling api routes
router = APIRouter()


@router.post("/login", response_description="login a user")
def login(user: Login):
    user_login = db.session.query(UserModel).filter_by(email=user.email).first()
    if user_login is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not Hash.verify(user_login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    # setting active status
    user_active = (
        db.session.query(UserModel)
        .filter_by(email=user.email)
        .update({"disabled": False})
    )
    db.session.commit()

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@router.post("/logout", response_description="logout a user")
def logout(user: dict = Depends(get_current_user)):
    print(user)
    user_logout = (
        db.session.query(UserModel)
        .filter_by(email=user["email"])
        .update({"disabled": True})
    )
    db.session.commit()
    user_out = {"user": user["username"], "status": "logged out"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_out)


@router.get("/me", response_description="Get details of currently logged in user")
async def get_me(user: dict = Depends(get_current_user)):
    return user


@router.post("/signup", response_model=User, response_description="logout a user")
def signup(user: User):
    new_user = UserSignupHandler(user).add_user_to_db()
    created_user = {"user": user.first_name, "status": "created"}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
