import re
from datetime import datetime
from itertools import count

class Post:
    MAX_POST_LENGTH = 300
    id_counter = count(1)

    def __init__(self, author, text, post_id=None, timestamp=None):
        """
        Create a post length 1-300 characters
        ValueError: if text is empty or too long
        """
        text = text.strip()
        if not text:
            raise ValueError("Your post can't be empty!")
        if len(text) > Post.MAX_POST_LENGTH:
            raise ValueError("There's too much text in your post!")
        if post_id is None:
            post_id = next(Post.id_counter)
        if timestamp is None:
            timestamp = datetime.now()
        self.id = post_id 
        self.author = author
        self.text = text
        self.timestamp = timestamp

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
    
    def to_dict(self):
        """
        Turn the post into a String to be saved in JSON can save
        """
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "timestamp": self.timestamp.isoformat()
        }