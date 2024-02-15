import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug import security

from applications.cheap_flights.forms import CheapFlights
from website_forms import LoginForm, RegisterForm

"""Imports from cheap_flights"""
from applications.cheap_flights.flights_search import search_flights

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

#TODO remember to invert app.config prior to commit
""" SQLALCHEMY """
#app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_INT_URL", "sqlite:///db_douglastopython.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
db.init_app(app)


""" DATABASE """
#TODO:
# Review ID, if required
# Create relationship in between databases
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

#TODO:
# Create relationship in between databases
class FlightsTrack(db.Model):
    __tablename__ = "flights_track"
    id = db.Column(db.Integer, primary_key=True)
    fly_from = db.Column(db.String(100))
    fly_to = db.Column(db.String(100))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    return_from = db.Column(db.Date)
    return_to = db.Column(db.Date)
    nights_in_dst_from = db.Column(db.Integer)
    nights_in_dst_to = db.Column(db.Integer)
    adults = db.Column(db.Integer)


with app.app_context():
    db.create_all()

""" LOGIN Handler """
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/")
def home():
    current_year = datetime.now().year
    return render_template("main.html", year=current_year)

@app.route("/cheap_flights", methods=["GET", "POST"])
def cheap_flight():
    form_cf = CheapFlights()
    if form_cf.is_submitted():
        """ IF to identify duplicated airport """
        if form_cf.fly_to.data == form_cf.fly_from.data:
            flash("Please select different Origin and Destination airports.", "error")
        else:
            """
            Flight search with values in Tequila API using POST FORM data
            """
            flights_result, status_code = search_flights(
                fly_from=form_cf.fly_from.data.split()[0],
                fly_to=form_cf.fly_to.data.split()[0],
                date_from=form_cf.date_from.data,
                date_to=form_cf.date_to.data,
                return_from=form_cf.return_from.data,
                return_to=form_cf.return_to.data,
                nights_in_dst_from=form_cf.nights_in_dst_from.data,
                nights_in_dst_to=form_cf.nights_in_dst_to.data,
                adults=form_cf.adults.data
            )
            """added status_code to format the output for user on html per status_code msg """
            return render_template("cheap_flights_result.html", flights_result=flights_result, status_code=status_code)
    return render_template("cheap_flights.html", form=form_cf)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """
    Sign Up user process.

    This function receives form submitted by the user.
    It checks if the username or email exists in the database.
    If the user does not exist:
        it registers the new user and returns a welcome page.
    If the user already exists:
        it displays an appropriate error message.

    :returns:
    successful registration: the function renders "sign_up_welcome.html".
    validation errors or user already exists: the function flashes errors on "sign_up.html".

    """

    reg_form = RegisterForm()
    if reg_form.is_submitted():
        user_exist = User.query.filter(
            (User.email == reg_form.username.data) | (User.username == reg_form.email.data)).first()
        if user_exist:
            if reg_form.username.data == user_exist.username:
                flash("Username already in use.")
            elif reg_form.email.data == user_exist.email:
                flash("Email already registered")
        else:
            new_user = User(
                username = reg_form.username.data.lower(),
                password = security.generate_password_hash(reg_form.password.data, method="pbkdf2", salt_length=8),
                email = reg_form.email.data.lower()
            )
            db.session.add(new_user)
            db.session.commit()

            return render_template("sign_up_welcome.html")
    return render_template("sign_up.html", form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.is_submitted():
        """Find/Filter User data"""
        user_exist = User.query.filter_by(email=login_form.user_authentication.data).first()
        if not user_exist:
            user_exist = User.query.filter_by(username=login_form.user_authentication.data).first()
        if user_exist:
            if not security.check_password_hash(user_exist.password, login_form.password.data):
                flash("Wrong password, try again.")
                return redirect(url_for("login"))
            else:
                login_user(user_exist)
                return render_template("login_welcome.html")

        flash("Username/Email does not exist.")
        return redirect(url_for ("login"))
    return render_template("login.html", form=login_form, current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/example")
@login_required
def example():
    return render_template("example.html")

@app.route("/until_here")
def until_here():
    return render_template("until_here.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
