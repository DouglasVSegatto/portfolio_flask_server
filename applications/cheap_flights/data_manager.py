from datetime import datetime


def update_airline_name(airline_id) -> str:
    """
    Update airline IDs to their corresponding names using a predefined dictionary.

    :param:
    airline_id(str): The airline ID to be updated.

    :returns:
    str: A string containing the updated airline name OR the original ID if not found.

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

    :param:
    flight_routes: A list of dictionaries with  flight route information.

    :return:
    List[str]: A list of formatted strings representing each flight route

    Notes:
    format_datetime function converts local_departure and local_arrival to a human-readable str
    """

    def format_datetime(datetime_str) -> str:
        """
        Format a datetime_str into a human-readable(str).

        Args:
            datetime_str (int): timestamp from API data.

        Returns:
            str: A string with formatted datetime ("DD/MM/YY at HH:MM").
        """

        date = datetime.fromtimestamp(datetime_str)
        return date.strftime('%d/%m/%y at %H:%M')

    full_route_str = []
    for route in flight_routes:
        fly_from = route["flyFrom"]
        city_from = route["cityFrom"]
        fly_to = route["flyTo"]
        city_to = route["cityTo"]
        local_departure = format_datetime(route["dTime"])
        local_arrival = format_datetime(route["aTime"])
        flight_no = route["flight_no"]
        airline = update_airline_name(route["airline"])

        # full_route_str.append(
        #     f"{update_airline_name(route['airline'])} | "
        #     f"Flight number: {route['flight_no']} - "
        #     f"{route['flyFrom']}({route['cityFrom']}) to {route['flyTo']}({route['cityTo']}) - "
        #     f"Departure: {format_datetime(route['dTime'])} - Arrival: {format_datetime(route['aTime'])}.")

        full_route_str.append(
            f"{airline} | "
            f"Flight number: {flight_no} - "
            f"{fly_from}({city_from}) to {fly_to}({city_to}) - "
            f"Departure: {local_departure} - Arrival: {local_arrival}.")
    return full_route_str
