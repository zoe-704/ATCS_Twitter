import pytest
from user import User, AlreadyFollowingError, NotFollowingError, SelfFollowError

def test_follow():
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    ellen.follow(zoe)
    assert zoe in ellen.following
    assert ellen in zoe.followers

def test_friend_follows_back():
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    ellen.follow(zoe)
    zoe.follow(ellen)
    assert ellen in zoe.following
    assert zoe in ellen.followers

def test_follow_twice():
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    ellen.follow(zoe)
    with pytest.raises(SelfFollowError):
        ellen.follow(ellen)

def test_unfollow():        
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    ellen.follow(zoe)
    ellen.unfollow(zoe)
    assert zoe not in ellen.following
    assert ellen not in zoe.followers

def test_unfollow_when_not_following():
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    with pytest.raises(NotFollowingError):
        ellen.unfollow(zoe)

def test_remove_all_follows():
    ellen = User("ellensakoda", "pw1", "Ellen", 16)
    zoe = User("zoesun", "pw2", "Zoe", 17)
    ellen.follow(zoe)
    zoe.follow(ellen)
    ellen.remove_all_follows()
    assert ellen.following == []
    assert ellen.followers == []
    assert zoe.following == []
    assert zoe.followers == []