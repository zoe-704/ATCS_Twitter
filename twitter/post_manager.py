import json
from datetime import datetime
from itertools import count
from post import Post

class PostManager:
    def __init__(self, filename):
        # List of all posts
        self.filename = filename
        self.all_posts = []

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump([post.to_dict() for post in self.all_posts], f, indent=4)

    def create_post(self, author, text):
        """
        Creates a new post for author
        """
        new_post = Post(author, text)
        self.all_posts.append(new_post)
        author.add_post(new_post)
        self.save_to_file()
        return new_post
    
    def get_post(self, post_id):
        """
        Find a post by its post_id
        """
        for post in self.all_posts:
            if post.id == post_id:
                return post
        return None
    
    def get_all_posts(self):
        """
        Returns every post, newest first
        """
        return sorted(self.all_posts, key=lambda post: post.id, reverse=True)
    
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
        self.save_to_file()

    def load_from_file(self, users):
        """
        Bring back saved posts from JSON file
        """
        # Read file
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        # Rebuild each post
        self.all_posts = []
        for info in data:
            user = users.get(info["author"])
            if user is None:
                # Author's account was deleted, so skip the post
                continue
            post = Post(
                user, 
                info["text"], 
                post_id=info["id"], 
                timestamp=datetime.fromisoformat(info["timestamp"])
            )
            self.all_posts.append(post)
            user.add_post(post) # keep user's own list in sync 

        # Make new IDs start after the highest saved ID
        if self.all_posts:
            highest_id = max(post.id for post in self.all_posts)
            Post.id_counter = count(highest_id + 1)
