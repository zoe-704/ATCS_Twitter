class Search:
    def __init__(self, accounts, posts):
        self.accounts = accounts
        self.posts = posts

    def search_user(self, search_text):
        # If the text does not start with an @ it does not count as a username
        if not search_text.startswith("@"):
            return None
        # Remove the @ symbol and return the valid username
        username = search_text[1:]
        return self.accounts.users.get(username)