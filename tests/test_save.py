import json
from itertools import count
import pytest
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

@pytest.fixture
def ellen():
    return User("ellensakoda", "pw1", "Ellen", 16)


# Test if json saves successfully
def test_create_post_writes_file(manager, path, zoe):
    manager.create_post(zoe, "hello")
    data = json.loads(path.read_text())
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["author"] == "zoesun"
    assert data[0]["text"] == "hello"

def test_multiple_posts_saved(manager, path, zoe):
    manager.create_post(zoe, "one")
    manager.create_post(zoe, "two")
    data = json.loads(path.read_text())
    assert [post["text"] for post in data] == ["one", "two"]

def test_delete_updates_file(manager, path, zoe):
    manager.create_post(zoe, "keep me")
    manager.create_post(zoe, "delete me")
    manager.delete_post(zoe, 2)
    data = json.loads(path.read_text())
    assert len(data) == 1
    assert data[0]["text"] == "keep me"

def test_round_trip(manager, path, zoe):
    original = manager.create_post(zoe, "saved post")

    # Simulate restarting the app with a new manager and a freshly loaded user
    new_zoe = User("zoesun", "pw2", "Zoe", 17)
    new_manager = PostManager(path)
    new_manager.load_from_file({"zoesun": new_zoe})

    loaded = new_manager.get_post(original.id)
    assert loaded is not None
    assert loaded.text == "saved post"
    assert loaded.author is new_zoe
    assert loaded.timestamp == original.timestamp

# Makes sure that reloaded posts are back on user profile
def test_load_adds_to_user_posts(manager, path, zoe):
    manager.create_post(zoe, "one")
    manager.create_post(zoe, "two")

    new_zoe = User("zoesun", "pw2", "Zoe", 17)
    PostManager(path).load_from_file({"zoesun": new_zoe})
    assert len(new_zoe.posts) == 2

def test_ids_continue_after_load(manager, path, zoe):
    manager.create_post(zoe, "one")
    manager.create_post(zoe, "two")

    # Restarting the app would reset the counter back to 1
    Post.id_counter = count(1)
    new_zoe = User("zoesun", "pw2", "Zoe", 17)
    new_manager = PostManager(path)
    new_manager.load_from_file({"zoesun": new_zoe})

    new_post = new_manager.create_post(new_zoe, "three")
    assert new_post.id == 3


# Tests for failed saves
def test_empty_post_not_saved(manager, path, zoe):
    with pytest.raises(ValueError):
        manager.create_post(zoe, "   ")
    assert manager.get_all_posts() == []
    assert zoe.posts == []
    assert not path.exists()

def test_too_long_post_not_saved(manager, path, zoe):
    with pytest.raises(ValueError):
        manager.create_post(zoe, "a" * 301)
    assert manager.get_all_posts() == []
    assert not path.exists()

def test_exactly_max_length_saved(manager, path, zoe):
    manager.create_post(zoe, "a" * 300)
    data = json.loads(path.read_text())
    assert len(data[0]["text"]) == 300

# JSON file won't be affected by an invalid post
def test_failed_post_leaves_file_unchanged(manager, path, zoe):
    manager.create_post(zoe, "hello")
    before = path.read_text()
    with pytest.raises(ValueError):
        manager.create_post(zoe, "")
    assert path.read_text() == before

def test_delete_missing_id(manager, path, zoe):
    manager.create_post(zoe, "hello")
    before = path.read_text()
    with pytest.raises(ValueError): # post doesn't exist
        manager.delete_post(zoe, 999)
    assert path.read_text() == before

def test_delete_someone_elses_post(manager, path, zoe, ellen):
    manager.create_post(zoe, "zoe's post")
    before = path.read_text()
    with pytest.raises(PermissionError):
        manager.delete_post(ellen, 1)
    assert path.read_text() == before
    assert manager.get_post(1) is not None


# Tests for loading bad or missing files
def test_load_missing_file(manager, zoe):
    # File was never created, so loading shouldn't crash
    manager.load_from_file({"zoesun": zoe})
    assert manager.get_all_posts() == []

def test_load_corrupt_file(manager, path, zoe):
    path.write_text("not json")
    manager.load_from_file({"zoesun": zoe})
    assert manager.get_all_posts() == []

def test_load_skips_deleted_author(manager, path, zoe):
    manager.create_post(zoe, "hello")
    new_manager = PostManager(path) 
    new_manager.load_from_file({})  # author's account no longer exists with restarted, new post manager
    assert new_manager.get_all_posts() == []