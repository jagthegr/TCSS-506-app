from flask import render_template, request, jsonify, flash, redirect, url_for  # Added flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required  # Added Flask-Login imports
from . import main  # Import the blueprint from __init__.py
from ..utils.wikimedia import search_wikimedia  # Import the wikimedia search function
from app import db  # Import db instance
from app.forms import LoginForm, RegistrationForm  # Import forms
from app.models import User  # Import User model

from werkzeug.urls import url_parse  # Helper for redirect security

@main.route('/')
def index():
    return render_template('pages/index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':  # Security check for next_page
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('pages/login.html', title='Sign In', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
    return render_template('pages/register.html', title='Register', form=form)

@main.route('/dashboard')
@login_required  # Protect the dashboard route
def dashboard():
    # Add logic for dashboard if needed
    return render_template('pages/dashboard.html')

@main.route('/search')
def search():
    query = request.args.get('q')  # Get search query from URL parameter 'q'
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
    return render_template('pages/search_results.html', query=query, results=results)
