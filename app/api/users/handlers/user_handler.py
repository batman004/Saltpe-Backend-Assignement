from fastapi import HTTPException, status
from fastapi_sqlalchemy import db
from api.users.endpoints.serializers import User, Login
from api.users.endpoints.models import User as UserModel
from api.users.auth.hashing import Hash
from api.users.auth.jwt import create_access_token, create_refresh_token
from api.users.auth.utils import get_current_user
import re


class UserSignupHandler:
    def __init__(self, user):
        self.new_user = user

    def is_strong_password(self):
        return (
            len(self.new_user.password) >= 8
            and re.search(r"\d", self.new_user.password)
            and re.search(r"[A-Z]", self.new_user.password)
        )

    def is_valid_email(self):
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.fullmatch(email_regex, self.new_user.email)

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
            except:
                raise db_user.error


class UserLoginHandler(UserSignupHandler):

    # check if detailes entered are consistent with DB
    def verify_form(self):
        pass

    # generate
    def generate_token(self):
        pass

    # check if user is already logged in
    def is_active(self):
        pass

    # udate status of user in DB
    def login_update_db(self):
        pass
