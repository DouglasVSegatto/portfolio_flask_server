import json
import os

import requests

from .data_manager import format_flight_route

"""
Tequila is API been used here to pull flights route
"""

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
API_KEY_TEQUILA = os.environ.get("PYTHON_TEQUILA_APIKEY")
flights_report = []


def search_flights(**kwargs):
    """
    This main code, requests, reads and filter data based on status_code returned from API.

    status_code == 200: Data received, execute rest of the code and return Flights_route to User
    status_code == 400: Request not accepted, "error msg" will be passed to User
    status_code == else: "No flights available" will be prompted to User

    :param:
    kwargs: To handle many entries im using **kwargs and using .get to capture the data.
        - fly_from (str): Departure airport code.
        - fly_to (str): Arrival airport code.
        - date_from (str): Departure date from (YYYY-MM-DD format).
        - date_to (str): Departure date to (YYYY-MM-DD format).
        - return_from (str): Return date from (YYYY-MM-DD format).
        - return_to (str): Return date to (YYYY-MM-DD format).
        - nights_in_dst_from (int): Minimum number of nights at the destination.
        - nights_in_dst_to (int): Maximum number of nights at the destination.
        - adults (int): Number of adult passengers.
   :arg:
    body:Contains values passed by User and statics
    * I'm keeping some data static as its for personal purpose.
    response: HTTP response containing flight data.

    :returns:
    flights_report: contains all data filtered and cleaned.
    response.status_code: Used as parameter for different status code from server

    """

    fly_from = kwargs.get('fly_from')
    fly_to = kwargs.get('fly_to')
    date_from = kwargs.get('date_from')
    date_to = kwargs.get('date_to')
    return_from = kwargs.get('return_from')
    return_to = kwargs.get('return_to')
    nights_in_dst_from = kwargs.get('nights_in_dst_from')
    nights_in_dst_to = kwargs.get('nights_in_dst_to')
    adults = kwargs.get('adults')

    search_endpoint = f"{TEQUILA_ENDPOINT}/search"
    body = {
        'fly_from': fly_from,
        'fly_to': fly_to,
        'date_from': date_from,
        'date_to': date_to,
        "return_from": return_from,
        "return_to": return_to,
        "nights_in_dst_from": nights_in_dst_from,
        "nights_in_dst_to": nights_in_dst_to,
        "curr": "CAD",
        "selected_cabins": "C",
        "mix_with_cabins": "M",
        "adults": adults,
        "vehicle_type": "aircraft",
        "max_stopovers": 2
    }
    headers = {
        "apikey": API_KEY_TEQUILA,
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.get(search_endpoint, headers=headers, params=body)
    result = response.json()

    if response.status_code == 200:
        for data in result["data"]:
            if data["availability"]["seats"] and data["availability"]["seats"] >= adults:
                flights_report.append({"price": data["fare"]["adults"], "route": format_flight_route(data["route"])})
        return flights_report, response.status_code
    elif response.status_code == 400:
        return result, response.status_code
    else:
        return None, None
