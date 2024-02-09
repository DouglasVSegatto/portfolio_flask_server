from flask import Flask, render_template, redirect, url_for, flash
from datetime import datetime
from applications.cheap_flights.forms import CheapFlights
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from website_forms import RegisterForm,LoginForm
from flask_login import login_user, LoginManager, current_user,logout_user
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
import os

"""Imports from cheap_flights"""
from applications.cheap_flights.flights_search import search_flights

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

""" SQLALCHEMY """
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_INT_URL", "sqlite:///db_douglastopython.db")
db = SQLAlchemy()
db.init_app(app)


""" DATABASE """
#TODO:
# Review ID, if required
# Create relationship in between databases
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

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

""" ## """

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
    reg_form = RegisterForm()
    if reg_form.is_submitted():
        """Filter both, username and email"""
        exist_user = User.query.filter(
            (User.email == reg_form.username.data) | (User.username == reg_form.email.data)).first()
        """Treat the existing"""
        if exist_user:
            if reg_form.username.data == exist_user.username:
                flash("Username already in use.")
            elif reg_form.email.data == exist_user.email:
                flash("Email already registered")
        else:
            """Register the new user"""
            new_user = User(
                username = reg_form.username.data,
                password = reg_form.password.data,
                email = reg_form.email.data
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
        result = db.session.execute(db.select(User).where(User.email == login_form.email.data))
        exist_user = result.scalar()
        """Treat the existing"""
        if exist_user:
            if login_form.password.data is not exist_user.password:
                flash("Wrong password, try again.")
                return redirect(url_for("login"))
            else:
                return render_template("login_welcome.html")
        flash("Username/Email does not exist.")
        return redirect(url_for ("login"))
    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.debug = True
    app.run()
