import pytest
from itertools import count
from user import User
from post import Post
from post_manager import PostManager

# Marks function as a setup provider
@pytest.fixture(autouse=True) # Runs before every test
def reset_ids():
    # Restart post IDs at 1 for every test
    Post.id_counter = count(1)
    
@pytest.fixture
def path(tmp_path):
    # Temporary file so tests don't overwrite the real post.json
    return tmp_path / "posts.json"

@pytest.fixture
def manager(path):
    return PostManager(path)

@pytest.fixture
def zoe():
    return User("zoesun", "pw2", "Zoe", 17)

def test_no_posts_yet(manager):
    assert manager.get_all_posts() == []

def test_newest_first(manager, zoe):
    manager.create_post(zoe, "first")
    manager.create_post(zoe, "second")
    manager.create_post(zoe, "third")
    ids = [post.id for post in manager.get_all_posts()]
    assert ids == [3, 2, 1]
    
def test_get_post_found(manager, zoe):
    post = manager.create_post(zoe, "hello")
    assert manager.get_post(1) is post

def test_get_post_missing(manager):
    assert manager.get_post(999) is None

def test_post_added_to_author(manager, zoe):
    post = manager.create_post(zoe, "hello")
    assert post in zoe.posts

def test_deleted_post_not_shown(manager, zoe):
    post = manager.create_post(zoe, "hello")
    manager.delete_post(zoe, post.id)
    assert post not in manager.get_all_posts()
    assert post not in zoe.posts

def test_post_display(manager, zoe):
    post = manager.create_post(zoe, "hello world")
    text = str(post)
    assert "@zoesun" in text
    assert "#1" in text
    assert "hello world" in text