class UserHandler:
    def __init__(self, f_name, l_name, email, password) -> None:
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password

    def validate_input(self):
        pass

    def verify_password(self):
        pass

    def user_exists(self):
        pass

    def generate_token(self):
        pass
