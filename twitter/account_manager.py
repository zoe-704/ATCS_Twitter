import json
from user import User

class AgeTooLowError(Exception):
    """Raised when the user age is too low."""
    pass

class AccountManager:
    def __init__(self, filename="users.json"):
        # JSON file where accounts are saved
        self.filename = filename
        # Dictionary - username: User
        self.users = {}
        self.current_user = None
        # Bring back accounts
        try:
            self.load_from_file()
        except FileNotFoundError:
            self.users = {}    

    def create_account(self, username, password, name, age):
        # Returns true if account made
        if age < 13:
            raise AgeTooLowError("You need to be 13 to create an account!")
        # Checks if username already exists
        if username in self.users:
            return False
        new_account = User(username, password, name, age)
        self.users[username] = new_account
        self.save_to_file()
        # Account succesfully made!
        return True

    def login(self, username, password):
        # Returns true if login succesful
        user = self.users.get(username)
        if user is None:
            return False
        if not user.check_password(password):
            return False
        # Login passes both username and password - create account
        self.current_user = user
        return True

    def logout(self):
        self.current_user = None

    def save_to_file(self):
        data = {}
        for username, user in self.users.items():
            data[username] = {
                "password": user.password,
                "name": user.name,
                "age": user.age
            }    
        with open(self.filename, "w")as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        self.users = {}
        for username, info in data.items():
            self.users[username] = User(username, info["password"], info["name"], info["age"])        

    def delete_account(self, post_manager=None):
        user = self.current_user
        if user is None:
            return False
        # Delete all posts
        if post_manager is not None:
            post_manager.all_posts = [p for p in post_manager.all_posts if p.author is not user]
            user.posts.clear()
        # Remove them from followers/followings
        for other in user.following:
            if user in other.followers:
                other.followers.remove(user)
        for other in user.followers:
            if user in other.following:
                other.following.remove(user)
        user.following.clear()
        user.followers.clear()
        # Remove account and log out                    
        del self.users[user.username]
        self.logout()
        self.save_to_file()
        return True