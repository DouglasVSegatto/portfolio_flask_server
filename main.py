import os
from datetime import datetime
from threading import Thread

from flask import Flask, flash, redirect, render_template, send_file, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

import forms
from forms import CheapFlights, Img2Pdf, LoginForm, RegisterForm, UnitConverter
from global_functions import upload_file_path, set_punctuation

from applications.cheap_flights.flights_search import search_flights

from applications.pdf_converter.data_manager import (delete_files,
                                                     generate_download_link,
                                                     image2pdf, pdf2image)
from applications.unit_converter.data_manager import km_to_miles,miles_to_km,l_per_100km_to_km_per_l,mpg_to_km_per_100

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO remember to invert app.config prior to commit
""" SQLALCHEMY """
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_INT_URL", "sqlite:///db_douglastopython.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
db.init_app(app)

""" DATABASE """


# TODO:
# Review ID, if required
# Create relationship in between databases
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)


# TODO:
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
    """
    Main website page call.

    :return: Current year.
    :rtype: int
    """
    current_year = datetime.now().year
    return render_template("main.html", year=current_year)


@app.route("/cheap_flights", methods=["GET", "POST"])
def cheap_flight():
    """
    Displays a form for searching cheap flights and forward the submitted form data.

    If the form is submitted:
        Function checks origin airport and destination airport are different.
            If they are the same, it displays an error message.
            If they are different, it processed with request, using the provided parameters.

    Flight search is performed using values from the submitted form,
    which are sent to the Tequila API via a POST request.

    :return: If the form is submitted
                flights_result returns a list to be rendered in search results.
                status_code returns status code from request in INT
                    if status == 200: good
                    if status == 400: flights_result will be a dict with invalid parameters explained.
    :rtype: list,int or dict,int
    """
    form_cf = CheapFlights()
    if form_cf.is_submitted():
        if form_cf.fly_to.data == form_cf.fly_from.data:
            flash("Please select different Origin and Destination airports.", "error")
        else:
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
            return render_template("cheap_flights_result.html", flights_result=flights_result, status_code=status_code)
    return render_template("cheap_flights.html", form=form_cf)


@app.route("/pdf_converter", methods=["GET", "POST"])
def pdf_converter():
    form_pdfconverter = Img2Pdf()
    if form_pdfconverter.is_submitted():
        filename = form_pdfconverter.file.data.filename
        form_pdfconverter.file.data.save(upload_file_path(filename))
        if form_pdfconverter.conversion.data == "pdf_to_image":
            validate = pdf2image(filename)
            if validate:
                download_link = generate_download_link(filename)
                delete_thread = Thread(target=delete_files, args=(filename,))
                delete_thread.start()
                return render_template("pdf_converter_result.html", download_urls=download_link)
            else:
                flash("Wrong file type, please upload a valid PDF file")
        elif form_pdfconverter.conversion.data == "image_to_pdf":
            validate = image2pdf(filename)
            if validate:
                download_link = generate_download_link(filename)
                delete_thread = Thread(target=delete_files, args=(filename,))
                delete_thread.start()
                return render_template("pdf_converter_result.html", download_urls=download_link)
            else:
                flash("Wrong file type, please upload a valid JPG/PNG file")
        else:
            flash("An error occur, please try again in a few minutes")
    return render_template("pdf_converter.html", form=form_pdfconverter)


@app.route("/download/<folder>/<filename>", methods=["GET"])
def download_file(folder, filename):
    converted_path = f"static/download/{folder}/{filename}"
    return send_file(converted_path, as_attachment=True)


@app.route("/unit_converter", methods=["GET", "POST"])
def unit_converter():
    """
    Converts the value passed based on the selected unit conversion.

    If the form is validated:
        - Determines the type of unit conversion selected and performs the conversion accordingly.
        - The result is formatted using the set_punctuation function before being displayed.

    Returns:
        str: Rendered HTML template containing the form for unit conversion.

    Note:
        - Each form submission triggers a unit conversion,
        however some conversions may reuse calculations to achieve the result.
        - Flash messages are used to display the result.

    """
    form_unitconverter = UnitConverter()
    if form_unitconverter.validate_on_submit():
        if form_unitconverter.conversion.data == "km_to_mile":
            result = km_to_miles(form_unitconverter.value.data)
            flash(set_punctuation(result))
            flash("miles")
        elif form_unitconverter.conversion.data == "mile_to_km":
            result = miles_to_km(form_unitconverter.value.data)
            flash(set_punctuation(result))
            flash("km")
        elif form_unitconverter.conversion.data == "liter100_to_kmliter":
            result = l_per_100km_to_km_per_l(form_unitconverter.value.data)
            flash(set_punctuation(result))
            flash("km/L")
        elif form_unitconverter.conversion.data == "mpg_to_km_per_100":
            result = mpg_to_km_per_100(form_unitconverter.value.data)
            flash(set_punctuation(result))
            flash("km/100L")
        elif form_unitconverter.conversion.data == "mpg_to_km_per_l":
            result = l_per_100km_to_km_per_l(mpg_to_km_per_100(form_unitconverter.value.data))
            flash(set_punctuation(result))
            flash("km/L")
    return render_template("unit_converter.html", form=form_unitconverter)


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
                username=reg_form.username.data.lower(),
                password=security.generate_password_hash(reg_form.password.data, method="pbkdf2", salt_length=8),
                email=reg_form.email.data.lower()
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
        return redirect(url_for("login"))
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
