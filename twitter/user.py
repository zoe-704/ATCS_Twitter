class AlreadyFollowingError(Exception):
    # Raised when a user tries to follow someone they already follow
    pass

class NotFollowingError(Exception):
    # Raised when a user tries to unfollow someone they don't follow
    pass

class SelfFollowError(Exception):
    # Raised when a user tries to follow or unfollow themselves
    pass

class User:
    def __init__(self, username, password, name, age):
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.posts = []
        self.following = []
        self.followers = []

    def check_password(self, password_guess):
        return self.password == password_guess

    def add_post(self, post):
        self.posts.append(post)

    def is_following(self, other):
        return other in self.following

    def follow(self, other):
        if other is self:
            raise SelfFollowError("You can't follow yourself!")
        if self.is_following(other):
            raise AlreadyFollowingError(f"You already following @{other.username}!")
        # Add other user to users following and add the user to the other users followers
        self.following.append(other)
        other.followers.append(self)

    def unfollow(self, other):
        if other is self:
            raise SelfFollowError("You can't unfollow yourself!")
        if not self.is_following(other):
            raise NotFollowingError(f"You don't follow @{other.username}!")
        # Remove other user from users following and remove the user from the other users followers
        self.following.remove(other)
        other.followers.remove(self)

    def remove_all_follows(self):
        # Remover all users in a user's following and followers - for delete account
        for other in list(self.following):
            self.unfollow(other)
        for other in list(self.followers):
            other.unfollow(self)    