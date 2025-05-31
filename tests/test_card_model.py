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


def test_create_card(db):
    user = Member(username="carduser", email="carduser@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Card Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    card = Card(question="What is 2+2?", answer="4", deck=deck)
    db.session.add(card)
    db.session.commit()
    queried = Card.query.filter_by(question="What is 2+2?").first()
    assert queried is not None
    assert queried.deck == deck


def test_card_repr(db):
    user = Member(username="reprcard", email="reprcard@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    card = Card(question="Q", answer="A", deck=deck)
    db.session.add(card)
    db.session.commit()
    assert repr(card).startswith(f"<Card {card.id} Q: Q")


def test_card_timestamp_default(db):
    user = Member(username="tstampcard", email="tstampcard@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    card = Card(question="Q", answer="A", deck=deck)
    db.session.add(card)
    db.session.commit()
    assert card.timestamp is not None


def test_card_deck_relationship(db):
    user = Member(username="relcard", email="relcard@example.com")
    user.set_password("pw")
    db.session.add(user)
    db.session.commit()
    deck = Deck(title="Rel Deck", author=user)
    db.session.add(deck)
    db.session.commit()
    card = Card(question="Q", answer="A", deck=deck)
    db.session.add(card)
    db.session.commit()
    assert card.deck == deck
    assert card in deck.cards.all()
