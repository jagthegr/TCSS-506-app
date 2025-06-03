from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    IntegerField,
    RadioField,  # Added RadioField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    NumberRange,  # Added NumberRange
)
from app.models import Member  # Assuming User model is in app/models/__init__.py


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Member.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = Member.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class GenerateFlashcardsForm(FlaskForm):
    topic = StringField(
        "Wikipedia Topic", validators=[DataRequired(), Length(min=1, max=140)]
    )
    num_cards = IntegerField(
        "Number of Cards",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        default=10,
    )
    generation_source = RadioField(
        "Generation Source",
        choices=[
            ("wikipedia", "Wikipedia (Agent)"),
            ("llm_wikipedia", "LLM (from Wikipedia Content)"),  # New option
        ],
        default="wikipedia",
        validators=[DataRequired()],
    )
    submit = SubmitField("Generate Flashcards")
