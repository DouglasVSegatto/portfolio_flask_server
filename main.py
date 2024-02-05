from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime
from applications.cheap_flights.forms import CheapFlights
from applications.cheap_flights.data_manager import DataManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5

"""Imports from cheap_flights"""
from applications.cheap_flights.flights_search import FlightSearch

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)


@app.route("/")
def home():
    current_year = datetime.now().year
    return render_template("main.html", year=current_year)


@app.route("/cheap_flights", methods=["GET", "POST"])
def cheap_flight():
    form_cf = CheapFlights()
    if form_cf.is_submitted():
        if form_cf.fly_to.data == form_cf.fly_from.data:
            flash("Please select different Origin and Destination airports.", "error")
        else:
            """
            Fligh search with values in Tequila API using POST FORM data
            """
            fs = FlightSearch()

            flights_result = fs.search_flights(
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
            print(flights_result)
            return render_template("cheap_flights_result.html", flights_result=flights_result)
    return render_template("cheap_flights.html", form=form_cf)


if __name__ == "__main__":
    app.debug = True
    app.run()
