from user import User

class AgeTooLowError(Exception):
    """Raised when the user age is too low."""
    pass

class AccountManager:
    def create_account(self, username, password, name, age):
        if age < 13:
            raise AgeTooLowError("You need to be 13 to create an account!")
        new_account = User(username, password, name, age)
