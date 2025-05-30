import pytest
from app import create_app
from app import db as _db

from app.models import Member  # relative import from current package


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "TESTING SECRET KEY"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


def test_create_member(db):
    user = Member(username="testuser", email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    queried = Member.query.filter_by(username="testuser").first()
    assert queried is not None
    assert queried.email == "test@example.com"


def test_unique_username_email(db):
    user1 = Member(username="uniqueuser", email="unique@example.com")
    user1.set_password("pw")
    db.session.add(user1)
    db.session.commit()
    user2 = Member(username="uniqueuser", email="other@example.com")
    user2.set_password("pw")
    db.session.add(user2)
    with pytest.raises(Exception):
        db.session.commit()
    db.session.rollback()
    user3 = Member(username="otheruser", email="unique@example.com")
    user3.set_password("pw")
    db.session.add(user3)
    with pytest.raises(Exception):
        db.session.commit()


def test_password_hash_and_check(db):
    user = Member(username="pwuser", email="pw@example.com")
    user.set_password("secretpw")
    db.session.add(user)
    db.session.commit()
    queried = Member.query.filter_by(username="pwuser").first()
    assert queried.check_password("secretpw")
    assert not queried.check_password("wrongpw")
    assert queried.password_hash != "secretpw"


def test_member_repr(db):
    user = Member(username="repruser", email="repr@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    assert "<User repruser>" == repr(user)


def test_member_decks_relationship(db):
    user = Member(username="deckuser", email="deck@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    # Should have no decks initially
    assert user.decks.count() == 0
