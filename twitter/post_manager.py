from post import Post

class PostManager:
    def __init__(self):
        # List of all posts
        self.all_posts = []

    def create_post(self, author, text):
        """
        Creates a new post for author
        """
        new_post = Post(author, text)
        self.all_posts.append(new_post)
        author.add_post(new_post)
        return new_post