"""
Originally i was going to try to scrape google flight for this information.
but i found the following site that provides and API that does pretty
much what i want.
"""

import datetime
from datetime import timedelta
import calendar
import requests
import json
import sys
import os
import inspect

#import the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from database_setup import Base, Flight

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


URL1 = "https://api.skypicker.com/flights?flyFrom="
URL2 = "&to="
URL3 = "&dateFrom="
URL4 = "&dateTo="
URL5 = "&partner=picky&one_per_date=1&curr=USD"

AIRPORTS = ["SFO", "JFK", "YXE"]
VEGAS = "LAS"

def main():
    #Let create 1 year worth of flight from today
    now = datetime.datetime.now()
    my_data = []
    for airport in AIRPORTS:
        print("Flight from " + airport + " to " + VEGAS)
        to_url = generate_url(now, airport, VEGAS)
        r = requests.get(to_url)
        parsed_json = json.loads(r.text)
        flights = parsed_json["data"]
        my_data = parse_flights(flights, my_data, airport, VEGAS)

        print("Flight from  " + VEGAS + " to " + airport)
        to_url = generate_url(now, VEGAS, airport)
        r = requests.get(to_url)
        parsed_json = json.loads(r.text)
        flights = parsed_json["data"]
        my_data = parse_flights(flights, my_data, VEGAS, airport)

def parse_flights(flights, my_data, start, end):
    for flight in flights:
        my_data.append({"start_airport": flight["flyFrom"],
                        "start_searched_airport": start,
                        "end_airport": flight["cityTo"],
                        "end_searched_airport": end,
                        "departure": datetime.datetime.fromtimestamp(flight["dTimeUTC"]),
                        "arrival": datetime.datetime.fromtimestamp(flight["aTimeUTC"]),
                        "price": flight["price"],
                        "link": flight["deep_link"],
                        "airline": flight["airlines"]
                        })
        add_flight_to_db(flight["flyFrom"],
                         start,
                         flight["cityTo"],
                         end,
                         datetime.datetime.fromtimestamp(flight["dTimeUTC"]),
                         datetime.datetime.fromtimestamp(flight["aTimeUTC"]),
                         flight["price"],
                         flight["deep_link"],
                         str(flight["airlines"]))
    return my_data

def add_flight_to_db(start, start_search, end, end_search, departure, arrival, price, link, airline):
    new_flight = Flight(start_ariport = start,
                        start_searched_airport = start_search,
                        end_airport = end,
                        end_searched_airport = end_search,
                        departure_time = departure,
                        arrival_time = arrival,
                        price = price,
                        link = link,
                        airline = airline)
    session.add(new_flight)
    session.commit()


def generate_url(date_obj, from_airport, to_airport):
    url = URL1 + from_airport + URL2 + to_airport + URL3
    url = url + date_obj.strftime("%d/%m/%Y") + URL4
    date_obj = date_obj + timedelta(days=365)
    last_day_of_month = str(calendar.monthrange(date_obj.year, date_obj.month)[1])
    url = url + last_day_of_month + date_obj.strftime("/%m/%Y") + URL5
    print(url)
    return url

if __name__ == "__main__":
    main()