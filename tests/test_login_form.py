import pytest
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import ValidationError
from app.forms import GenerateFlashcardsForm, LoginForm


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "TESTING SECRET KEY"


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture
def form_context(app):
    # Flask-WTF forms require a request context
    with app.test_request_context():
        yield


# --- GenerateFlashcardsForm Tests ---


def test_generate_flashcards_form_valid(form_context):
    form = GenerateFlashcardsForm(topic="Python", num_cards=10)
    assert form.errors == {}


def test_generate_flashcards_form_missing_topic(form_context):
    form = GenerateFlashcardsForm(topic="", num_cards=10)
    assert not form.validate()
    assert "This field is required." in form.topic.errors


def test_generate_flashcards_form_topic_too_long(form_context):
    long_topic = "A" * 141
    form = GenerateFlashcardsForm(topic=long_topic, num_cards=10)
    assert not form.validate()


def test_generate_flashcards_form_num_cards_below_min(form_context):
    form = GenerateFlashcardsForm(topic="Python", num_cards=0)
    assert not form.validate()


def test_generate_flashcards_form_num_cards_above_max(form_context):
    form = GenerateFlashcardsForm(topic="Python", num_cards=51)
    assert not form.validate()


def test_generate_flashcards_form_missing_num_cards(form_context):
    form = GenerateFlashcardsForm(topic="Python", num_cards=None)
    assert not form.validate()
    assert "This field is required." in form.num_cards.errors


# --- LoginForm Tests ---


def test_login_form_valid(form_context):
    form = LoginForm(username="user", password="password")
    assert form.errors == {}


def test_login_form_missing_username(form_context):
    form = LoginForm(username="", password="password")
    assert not form.validate()
    assert "This field is required." in form.username.errors


def test_login_form_missing_password(form_context):
    form = LoginForm(username="user", password="")
    assert not form.validate()
    assert "This field is required." in form.password.errors
