import pytest
from app.models import Deck, Member, Card
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


def test_create_deck(db):
    user = Member(username="deckowner", email="deckowner@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Test Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    queried = Deck.query.filter_by(title="Test Deck").first()
    assert queried is not None
    assert queried.author == user


def test_deck_repr(db):
    user = Member(username="reprdeck", email="reprdeck@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="DeckTitle", author=user)
    db.session.add(deck)
    db.session.commit()
    assert repr(deck) == "<Deck DeckTitle>"


def test_deck_cards_relationship(db):
    user = Member(username="carddeck", email="carddeck@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Card Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    card1 = Card(question="Q1", answer="A1", deck=deck)
    card2 = Card(question="Q2", answer="A2", deck=deck)
    db.session.add_all([card1, card2])
    db.session.commit()
    queried_deck = Deck.query.filter_by(title="Card Deck").first()
    assert queried_deck.cards.count() == 2
    questions = [card.question for card in queried_deck.cards]
    assert "Q1" in questions and "Q2" in questions


def test_deck_timestamp_default(db):
    user = Member(username="tstamp", email="tstamp@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Timestamp Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    assert deck.timestamp is not None
