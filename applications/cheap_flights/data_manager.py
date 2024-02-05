from datetime import datetime

class DataManager:
    """ Class responsible for accessing Google Sheet database """


    def update_airline_name(self, airline_id) -> str:

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
            "AA": "American Airlinas"
        }

        data = []


        if airline_id in airlines_dict:
            return airlines_dict[airline_id]
        else:
            return airline_id

    def FormatFlightRoute(self, flight_routes) -> list[str]:
        """ Format the flight route information into a string """

        def FormatDateTime(datetime_str):
            date = datetime.fromtimestamp(datetime_str)
            """ Format datetime object as string 'dd/mm/yy at 00:00 hours'"""
            return date.strftime('%d/%m/%y at %H:%M')

        formatted_text = []
        for route in flight_routes:
            fly_from = route["flyFrom"]
            city_from = route["cityFrom"]
            fly_to = route["flyTo"]
            city_to = route["cityTo"]
            local_departure = FormatDateTime(route["dTime"])
            local_arrival = FormatDateTime(route["aTime"])
            flight_no = route["flight_no"]
            airline = self.update_airline_name(route["airline"])
            formatted_text.append(f"{airline} | Flight number: {flight_no} - {fly_from}({city_from}) to {fly_to}({city_to}) - Departure: {local_departure} - Arrival: {local_arrival}")
        return formatted_text
