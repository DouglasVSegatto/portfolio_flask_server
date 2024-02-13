import os

import requests

from .data_manager import format_flight_route

"""
Tequila data
"""

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
API_KEY_TEQUILA = os.environ.get("PYTHON_TEQUILA_APIKEY")
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
flights_report = []


def search_flights(**kwargs):
    """
    To handle many entries im using **kwargs.
    using .get to handle empty/none values
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

    """
    I'm keeping some data static as its for personal purpose.
    PS: now its up to you for amount of people,
    if you change the amount adults variable it will filter considering available seats
    """
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
        # "ret_from_diff_city": False,
        # "ret_to_diff_city":True,
        "adults": adults,
        "vehicle_type": "aircraft",
        "max_stopovers": 0
    }
    headers = {
        "apikey": API_KEY_TEQUILA,
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.get(search_endpoint, headers=headers, params=body)
    result = response.json()
    print(response.status_code)
    print(result)

    """
    TOASK: I have many IFs here, whats best approach?
    * Move some data into a variable and do a filter from there
    * Keep adding IF (like current one)
    * Quit dev(LOL)
    """
    if response.status_code == 200:
        for data in result["data"]:
            if data["availability"]["seats"] is not None and data["availability"]["seats"] >= adults:
                flights_report.append({"price": data["fare"]["adults"], "route": format_flight_route(data["route"])})
        return flights_report, response.status_code
    elif response.status_code == 400:
        return result, response.status_code
    else:
        return None, None
