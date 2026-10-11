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

    def delete_post(self, author, post_id):
        """
        Deletes an author's post
        """
        post = self.get_post(post_id)
        # Check if possible to delete post
        if post is None:
            raise ValueError(f"Post #{post_id} doesn't exist.")
        if post.author is not author:
            raise PermissionError("You can only delete your own posts.")
        # Delete all instances of post
        self.all_posts.remove(post)
        author.posts.remove(post)   # keep the user's list in sync