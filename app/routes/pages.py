from flask import (
    render_template,
    request,
    jsonify,
    flash,
    redirect,
    url_for,
)  # Added flash, redirect, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)  # Added Flask-Login imports
from . import main  # Import the blueprint from __init__.py
from ..utils.wikimedia import (
    search_wikimedia,
    generate_flashcards_from_topic_agent,
)  # Updated imports
from ..utils.wikipedia_agent import get_wikipedia_page_content_for_llm # Import new helper
from ..utils.llm_flashcard_generator import generate_llm_flashcards # Added LLM import
from app import db  # Import db instance
from app.forms import (
    LoginForm,
    RegistrationForm,
    GenerateFlashcardsForm,
)  # Added GenerateFlashcardsForm
from app.models import Member, Deck, Card  # Added Deck and Card

from werkzeug.urls import url_parse  # Helper for redirect security
import logging # Import logging


@main.route("/")
def index():
    return render_template("pages/index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Member.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("main.login"))
        login_user(user, remember=form.remember_me.data)
        flash("Logged in successfully.", "success")
        next_page = request.args.get("next")
        if (
            not next_page or url_parse(next_page).netloc != ""
        ):  # Security check for next_page
            next_page = url_for("main.dashboard")
        return redirect(next_page)
    return render_template("pages/login.html", title="Sign In", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@main.route("/delete_account", methods=["POST", "GET"])
@login_required
def delete_account():
    if current_user.is_authenticated:
        try:
            db.session.delete(
                current_user
            )  # This will cascade delete associated decks and cards
            db.session.commit()
            flash("Your account has been deleted successfully.", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting account: {str(e)}", "danger")
            # Log the error e for debugging
            print(f"Error deleting account: {e}")
            return redirect(url_for("main.profile"))


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Member(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for("main.login"))
    return render_template("pages/register.html", title="Register", form=form)


@main.route("/dashboard")
@login_required  # Protect the dashboard route
def dashboard():
    user_decks = (
        Deck.query.filter_by(user_id=current_user.id)
        .order_by(Deck.timestamp.desc())
        .all()
    )
    return render_template("pages/dashboard.html", decks=user_decks)


@main.route("/deck/<int:deck_id>")
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    # Ensure the current user owns this deck
    if deck.author != current_user:
        flash("You don't have permission to view this deck.", "danger")
        return redirect(url_for("main.dashboard"))

    # Cards are accessible via deck.cards (due to the relationship)
    # If it's a lazy loaded relationship, cards will be fetched when accessed.
    # If you need to paginate or do more complex queries, you might query deck.cards directly.
    return render_template("pages/view_deck.html", deck=deck, cards=deck.cards.all())


@main.route("/deck/<int:deck_id>/delete", methods=["POST"])
@login_required
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.author != current_user:
        flash("You don't have permission to delete this deck.", "danger")
        return redirect(url_for("main.dashboard"))

    try:
        db.session.delete(
            deck
        )  # The cascade delete in the model will handle associated cards
        db.session.commit()
        flash(f'Deck "{deck.title}" has been deleted successfully.', "success")
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting deck "{deck.title}": {str(e)}', "danger")
        # Log the error e for debugging
        print(f"Error deleting deck: {e}")

    return redirect(url_for("main.dashboard"))


@main.route("/profile")
@login_required
def profile():
    return render_template("pages/profile.html", title="Profile")


@main.route("/settings")
@login_required
def settings():
    return render_template("pages/settings.html", title="Settings")


@main.route("/search")
def search():
    query = request.args.get("q")  # Get search query from URL parameter 'q'
    results = []
    if query:
        search_results = search_wikimedia(query)
        if search_results is None:
            # Handle API error appropriately, maybe flash a message or log
            print("Error fetching from Wikimedia API")
            results = []  # Ensure results is an empty list on error
        else:
            results = search_results
    # Render a template with the results
    return render_template("pages/search_results.html", query=query, results=results)


@main.route("/generate_flashcards", methods=["GET", "POST"])
@login_required
def generate_flashcards():
    form = GenerateFlashcardsForm()
    if form.validate_on_submit():
        topic = form.topic.data
        num_cards = form.num_cards.data
        source = form.generation_source.data

        extracted_cards = []
        deck_title_prefix = ""

        if source == 'wikipedia':
            deck_title_prefix = f"Flashcards on {topic} (Wikipedia)"
            # This agent returns list of tuples: (question, answer)
            raw_wiki_cards = generate_flashcards_from_topic_agent(
                topic, num_cards_desired=num_cards
            )
            # Convert to list of dicts for consistency, if needed, or handle differently in loop
            if raw_wiki_cards:
                for q, a in raw_wiki_cards:
                    extracted_cards.append({"front": q, "back": a})
        elif source == 'llm_wikipedia': # New option handler
            deck_title_prefix = f"Flashcards on {topic} (LLM from Wikipedia)"
            logging.info(f"Attempting to generate flashcards for '{topic}' using LLM from Wikipedia content.")
            wikipedia_content = get_wikipedia_page_content_for_llm(topic)
            if wikipedia_content:
                logging.info(f"Successfully fetched Wikipedia content for '{topic}' ({len(wikipedia_content)} chars). Now generating LLM flashcards.")
                extracted_cards = generate_llm_flashcards(wikipedia_content, num_flashcards=num_cards)
            else:
                logging.warning(f"Failed to fetch Wikipedia content for '{topic}'. Cannot generate LLM flashcards from Wikipedia.")
                flash(f"Could not retrieve Wikipedia content for '{topic}'. Please try a different topic or source.", "warning")
                return redirect(url_for("main.generate_flashcards"))
        else:
            flash("Invalid generation source selected.", "danger")
            return redirect(url_for("main.generate_flashcards"))

        if not extracted_cards:
            flash(
                f'Could not generate any flashcards for "{topic}" using {source.upper()}. The topic might not exist, be ambiguous, or the content may not be suitable for flashcard generation. Please try a different topic or source.',
                "warning",
            )
            return redirect(url_for("main.generate_flashcards"))

        try:
            new_deck = Deck(title=deck_title_prefix, author=current_user)
            db.session.add(new_deck)

            for card_data in extracted_cards:  # card_data is now a dict
                if isinstance(card_data, dict) and "front" in card_data and "back" in card_data:
                    new_card = Card(
                        question=card_data["front"],
                        answer=card_data["back"],
                        deck=new_deck
                    )
                    db.session.add(new_card)
                else:
                    print(f"Skipping malformed card data: {card_data} from {source}")

            db.session.commit()
            flash(
                f'{len(extracted_cards)} flashcards generated for "{topic}" using {source.upper()} and saved to a new deck!',
                "success",
            )
            return redirect(
                url_for("main.view_deck", deck_id=new_deck.id)
            )
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving flashcards: {str(e)}", "danger")
            print(f"Error saving {source}-generated flashcards: {e}")
            return redirect(url_for("main.generate_flashcards"))
    else:
        if request.method == "POST":
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        pass

    return render_template(
        "pages/generate_flashcards.html", title="Generate Flashcards", form=form
    )


# In your Flask app (example)
@main.route("/deck/<int:deck_id>/add_card", methods=["POST"])
def add_card(deck_id):
    question = request.form["question"]
    answer = request.form["answer"]

    new_card = Card(question=question, answer=answer, deck_id=deck_id)
    db.session.add(new_card)

    db.session.commit()
    flash(f'new flashcard added to "{deck_id}"', "success")
    return redirect(
        url_for("main.view_deck", deck_id=deck_id)
    )  # Redirect to the new deck


@main.route("/deck/<int:deck_id>/delete_card/<int:card_id>", methods=["POST"])
def delete_card(deck_id, card_id):
    card = Card.query.get_or_404(card_id)
    try:
        db.session.delete(
            card
        )  # The cascade delete in the model will handle associated cards
        db.session.commit()
        flash(f'Deck "{card.id}" has been deleted successfully.', "success")
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting deck "{card.title}": {str(e)}', "danger")
        # Log the error e for debugging
        print(f"Error deleting deck: {e}")

    return redirect(url_for("main.view_deck", deck_id=deck_id))


@main.route("/about")
def about_page():
    return render_template("./pages/about.html")
