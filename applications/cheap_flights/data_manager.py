from datetime import datetime


def update_airline_name(airline_id) -> str:

    """
    Update airline IDs to their corresponding names using a predefined dictionary.
    Args: - airline_id (List[str]): A list of airline IDs to be updated.
    Returns: - str: A string containing updated airline names or IDs joined by ', '.
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
        "AA": "American Airlinas",
        "4N": "Air North",
        "TK": "Turkish Airlines"
    }

    data = []

    if airline_id in airlines_dict:
        return airlines_dict[airline_id]
    else:
        return airline_id


def format_flight_route(flight_routes) -> list[str]:
    """ Format the flight route information into a string """

    def format_datetime(datetime_str):
        """ Format datetime object as string 'dd/mm/yy at 00:00 hours'"""
        date = datetime.fromtimestamp(datetime_str)
        return date.strftime('%d/%m/%y at %H:%M')

    formatted_routes = []
    for route in flight_routes:
        airline = update_airline_name(route["airline"])
        local_departure = format_datetime(route["dTime"])
        local_arrival = format_datetime(route["aTime"])

        formatted_route = (f"{airline} | "
                           f"Flight number: {route['flight_no']} - "
                           f"{route['flyFrom']}({route['cityFrom']}) to {route['flyTo']}({route['cityTo']}) - "
                           f"Departure: {local_departure} - "
                           f"Arrival: {local_arrival}. ")

        formatted_routes.append(formatted_route)

    return formatted_routes

