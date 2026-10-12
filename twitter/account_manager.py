import json
from user import User
from post import Post

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
                "age": user.age,
                "following" : [other.username for other in user.following]
            }    
        with open(self.filename, "w")as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        self.users = {}
        # Make every user
        for username, info in data.items():
            self.users[username] = User(username, info["password"], info["name"], info["age"]) 
        # Reconnect follows once all users exist again    
        for username, info in data.items():
            user = self.users[username]
            for other_name in info.get("following", []):
                other = self.users.get(other_name)
                if other is not None and not user.is_following(other):
                    user.follow(other)       

    def delete_account(self, post_manager=None):
        user = self.current_user
        if user is None:
            return False
        # Delete all posts
        if post_manager is not None:
            post_manager.all_posts = [p for p in post_manager.all_posts if p.author is not user]
            user.posts.clear()
            post_manager.save_to_file()
        # Remove them from followers/followings
        user.remove_all_follows()
        # Remove account and log out                    
        del self.users[user.username]
        self.logout()
        self.save_to_file()
        return True

    def follow_user(self, username):
        # Lstrip removes @ symbol from the start until it reaches a character that isn't @
        # Thus, a username can be entered into this function with or without the @ symbol
        other = self.users.get(username.lstrip("@"))
        if self.current_user is None or other is None:
            return False
        self.current_user.follow(other)
        self.save_to_file()
        return True

    def unfollow_user(self, username):
        other = self.users.get(username.lstrip("@"))
        if self.current_user is None or other is None:
            return False
        self.current_user.unfollow(other)
        self.save_to_file()
        return True