from datetime import datetime


def update_airline_name(airline_id) -> str:
    """
    Update airline IDs to their corresponding names using a predefined dictionary.

    :param airline_id: The airline ID to be updated.
    :type airline_id: str
    :returns: A string containing the updated airline name OR the original ID if not found.
    :rtype: str
    """

    airlines_dict = {
        "AC": "Air Canada",
        "WS": "WestJet Airlines",
        "RV": "Air Canada Rouge",
        "QK": "Jazz Aviation LP (Air Canada Jazz)",
        "TS": "Air Transat",
        "PD": "Porter Airlines",
        "WR": "WestJet Encore",
        "WG": "Sunwing Airlines",
        "F8": "Flair Airlines",
        "Y9": "Linx Air",
        "LA": "LATAM Airlines",
        "AA": "American Airlines",
        "4N": "Air North",
        "TK": "Turkish Airlines"
    }

    try:
        return airlines_dict[airline_id]
    except KeyError:
        return str(airline_id)


def format_flight_route(flight_routes) -> list[str]:
    """
    Format flight_routes information into a string/text per route.

    :param flight_routes: A list of dictionaries with  flight route information.
    :type flight_routes: list
    :return: A list of formatted strings representing each flight route
    :rtype: list[str]

    Notes:
    format_datetime function converts local_departure and local_arrival to a human-readable str
    """

    def format_datetime(date_time) -> str:
        """
        Format and returns a human-readable(str).

        :param date_time: timestamp from API data.
        :type date_time: int
        :return: A string with formatted datetime ("DD/MM/YY at HH:MM").
        :rtype: str
        """
        date = datetime.fromtimestamp(date_time)
        return date.strftime('%d/%m/%y at %H:%M')

    full_route_str = []
    for route in flight_routes:
        airline = update_airline_name(route["airline"])
        local_departure = format_datetime(route["dTime"])
        local_arrival = format_datetime(route["aTime"])
        full_route_str.append(
            f"{airline} | "
            f"Flight number: {route['flyFrom']} - "
            f"{route['cityFrom']}({route['cityFrom']}) to {route['flyTo']}({route['cityTo']}) - "
            f"Departure: {local_departure} - Arrival: {local_arrival}.")
    return full_route_str
