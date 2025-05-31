import pytest
from app.forms import RegistrationForm
from app.models import Member
from app import create_app
from app import db as _db


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


@pytest.fixture
def client(app):
    return app.test_client()


def test_registration_form_valid(db):
    form = RegistrationForm(
        username="excited_user",
        email="newuser@example.com",
        password="password456",
        password2="password456",
    )

    assert form.errors == {}


def test_registration_form_duplicate_username(db):
    user = Member(username="existinguser", email="user1@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    form = RegistrationForm(
        username="existinguser",
        email="newemail@example.com",
        password="password123",
        password2="password123",
    )
    assert not form.validate()
    assert "Please use a different username." in form.username.errors


def test_registration_form_duplicate_email(db):
    user = Member(username="user2", email="existing@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    form = RegistrationForm(
        username="newuser2",
        email="existing@example.com",
        password="password123",
        password2="password123",
    )
    assert not form.validate()
    assert "Please use a different email address." in form.email.errors


def test_registration_form_password_mismatch(db):
    form = RegistrationForm(
        username="user3",
        email="user3@example.com",
        password="password123",
        password2="differentpassword",
    )
    assert not form.validate()
    assert "Field must be equal to password." in form.password2.errors


def test_registration_form_short_password(db):
    form = RegistrationForm(
        username="user4",
        email="user4@example.com",
        password="short",
        password2="short",
    )
    assert not form.validate()
    assert any(
        "Field must be at least" in err or "shorter than" in err
        for err in form.password.errors
    )


def test_registration_form_invalid_email(db):
    form = RegistrationForm(
        username="user5",
        email="not-an-email",
        password="password123",
        password2="password123",
    )
    assert not form.validate()
    assert "Invalid email address." in form.email.errors
