import re
from datetime import datetime
from itertools import count

class Post:
    MAX_POST_LENGTH = 300
    id_counter = count(1)

    def __init__(self, author, text):
        """
        Create a post length 1-300 characters
        ValueError: if text is empty or too long
        """
        text = text.strip()
        if not text:
            raise ValueError("Your post can't be empty!")
        if len(text) > Post.MAX_POST_LENGTH:
            raise ValueError("There's too much text in your post!")
        self.id = next(Post.id_counter) 
        self.author = author
        self.text = text
        self.timestamp = datetime.now()

    def __str__(self):
        time = self.timestamp.strftime("%b %d, %I:%M %p")
        return f"[#{self.id}] @{self.author.username}, {time}\n  {self.text}"

    def contains_hashtag(self, tag):
        """
        Check if a post contains a hashtag of a word (with or without '#')
        Returns whether or not hashtag appears in the post
        """
        tag = tag.lstrip("#").lower()
        hashtags = re.findall(r"#(\w+)", self.text.lower())
        return tag in hashtags