from data_manager import DataManager
from flights_search import FlightSearch
from datetime import datetime,timedelta
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, NotificationManager classes to achieve the program requirements.
"""
Currently not setting dates manually:
We're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6x30days) time. 
We're also looking for round trips that return between 7 and 28 days in length
"""
adults = 1
dm = DataManager()
fd = FlightSearch()
nc = NotificationManager()
TXT_MSG = "Low Price Alert! \n"

"""
Date and Time calculation Section
"""
# today = datetime.now()
# togo_tomorrow = today - timedelta(days=-1)
# togo_in_sixty_days = today + timedelta(days=6*30)
# comeback_in_seven = today + timedelta(days=7)
# comeback_in_twenty_eight = today + timedelta(days=28)

#TODO """ Get data from POST form """
adults =
fly_from =
fly_to =
date_from =
date_to =
return_from =
return_to =

    """
    Get values from Tequila API based on Google sheet
    Each search will be related to From/To in database
    """
    lowest_price, departure_city, arrival_city, departure_day, return_day, airline, flight_numb = fd.search_flights(
        iataCodeFrom,
        iataCodeTo,
        togo_tomorrow.strftime("%d/%m/%Y"),
        togo_in_sixty_days.strftime("%d/%m/%Y"),
        comeback_in_seven.strftime("%d/%m/%Y"),
        comeback_in_twenty_eight.strftime("%d/%m/%Y"),
        adults,
        average_price
    )
    """
    Confirm there is output on lowest_price
    Build one only text msg (sends one text msg with all offers found)
    Updates Sheet with lowest price found (might use it on future for user reference)
    """
    if lowest_price:
        airline = dm.update_airline_name(airline)
        TXT_MSG += (f"""{airline} - Only CAD${lowest_price} to fly from {departure_city} to {arrival_city},
                    from {departure_day} to {return_day}, flight number {flight_numb}\n""")
        if lowest_price < destine_list["lowestPrice"]:
            dm.update_flight_lowest_price(destine_list["id"], lowest_price)
            print(f"Found a Lowest Price from {departure_city} to {arrival_city}")
# print(TXT_MSG)
nc.send_text(TXT_MSG)
print("closing program")












