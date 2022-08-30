from fastapi import HTTPException, status
from fastapi_sqlalchemy import db
from sqlalchemy.exc import SQLAlchemyError
from api.users.endpoints.models import User as UserModel
from api.users.auth.hashing import Hash
from api.users.auth.jwt import create_access_token, create_refresh_token
from api.users.utils.blacklist_tokens import add_blacklist_token
from api.users.auth.utils import get_current_user
import re


class UserSignupHandler:
    def __init__(self, user):
        self.new_user = user

    def is_strong_password(self):
        if len(self.new_user.password) >= 8:
            return True
        return False

    def is_valid_email(self):
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(email_regex, self.new_user.email):
            return True
        return False

    def validate_input(self):
        if (
            not self.is_strong_password()
            or not self.new_user.username.isalnum()
            or not self.is_valid_email()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"please enter valid details",
            )
        else:
            return True

    def user_exists(self):
        user_search = (
            db.session.query(UserModel.email)
            .filter_by(email=self.new_user.email)
            .first()
        )

        if user_search is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email: '{self.new_user.email}' already exist",
            )

        return False

    def add_user_to_db(self):
        if not self.user_exists() and self.validate_input():
            try:
                db_user = UserModel(
                    first_name=self.new_user.first_name,
                    last_name=self.new_user.last_name,
                    email=self.new_user.email,
                    username=self.new_user.username,
                    password=Hash.bcrypt(self.new_user.password),
                    disabled=True,
                )
                db.session.add(db_user)
                db.session.commit()
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                return error


class UserLoginHandler:
    def __init__(self, user_login):
        self.user_login = user_login

    # check if detailes entered are consistent with DB
    def verify_credentials(self):
        user_login = (
            db.session.query(UserModel).filter_by(email=self.user_login.email).first()
        )
        if user_login is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
        if not Hash.verify(user_login.password, self.user_login.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )
        return True

    # generate token after validation and verification
    def generate_token(self):
        return {
            "access_token": create_access_token(self.user_login.email),
            "refresh_token": create_refresh_token(self.user_login.email),
        }

    # check if user is already logged in
    def is_active(self):
        if self.verify_credentials():
            user_active = (
                db.session.query(UserModel.disabled)
                .filter_by(email=self.user_login.email)
                .first()
            )
            if user_active.disabled == False:
                return True
            else:
                return False

    def login_user(self):
        if not self.is_active():
            print("new login")
            try:
                user_active = (
                    db.session.query(UserModel)
                    .filter_by(email=self.user_login.email)
                    .update({"disabled": False})
                )
                db.session.commit()
                return self.generate_token()
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                return error

        else:
            logged_in = self.generate_token()
            logged_in["status"] = "already logged in"
            return logged_in


class UserLogoutHandler:
    def __init__(self, current_user):
        self.current_user = current_user

    def update_status(self):
        try:
            user_logout = (
                db.session.query(UserModel)
                .filter_by(email=self.current_user["email"])
                .update({"disabled": True})
            )
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return error

    def blacklist_token(self):
        if add_blacklist_token(self.current_user["token"]):
            return True

    def logout_user(self):
        if self.update_status() and self.blacklist_token():
            user_out = {"user": self.current_user["username"], "status": "logged out"}
        return user_out
