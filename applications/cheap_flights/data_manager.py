from datetime import datetime


def update_airline_name(airline_id: str) -> str:
    """
    Update airline IDs to their corresponding names using a predefined dictionary.

    :param airline_id: A list of airline IDs to be updated.

    :return: A string containing updated airline names or IDs joined by ', '.
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

    data = []

    if airline_id in airlines_dict:
        return airlines_dict[airline_id]
    else:
        return airline_id


def format_flight_route(flight_routes) -> list[str]:
    """
    Format the flight route information into a string.

    :param flight_routes:

    :return:  A list of string-formatted flight routes.
    """

    def format_datetime(datetime_str: float) -> str:
        """Format datetime object as string 'dd/mm/yy at 00:00 hours'."""
        date = datetime.fromtimestamp(datetime_str)
        return date.strftime('%d/%m/%y at %H:%M')

    formatted_text = []
    for route in flight_routes:
        fly_from = route["flyFrom"]
        city_from = route["cityFrom"]
        fly_to = route["flyTo"]
        city_to = route["cityTo"]
        local_departure = format_datetime(route["dTime"])
        local_arrival = format_datetime(route["aTime"])
        flight_no = route["flight_no"]
        airline = update_airline_name(route["airline"])

        formatted_text.append(
            f"{airline} | Flight number: {flight_no} - {fly_from}({city_from}) to {fly_to}({city_to}) - Departure: {local_departure} - Arrival: {local_arrival}. ")

    return formatted_text

