"""
Originally i was going to try to scrape google flight for this information.
but i found the following site that provides and API that does pretty
much what i want.
"""

import datetime
import calendar
import requests
import json
import sys


URL1 = "https://api.skypicker.com/flights?flyFrom="
URL2 = "&to="
URL3 = "&dateFrom="
URL4 = "&dateTo="
URL5 = "&partner=picky&one_per_date=1&curr=USD"

AIRPORTS = ["SFO", "JFK"]
VEGAS = "LAS"

def main():
    #Let create 1 year worth of flight from today
    now = datetime.datetime.now()
    for airport in AIRPORTS:
        url = generate_url(now, airport)
        r = requests.get(url)
        parsed_json = json.loads(r.text)
        flights = parsed_json["data"]
        for flight in flights:
            print(flight["price"])
        sys.exit(1)


def generate_url(date_obj, airport):
    url = URL1 + airport + URL2 + VEGAS + URL3
    url = url + date_obj.strftime("%d/%m/%Y") + URL4
    last_day_of_month = str(calendar.monthrange(date_obj.year, date_obj.month)[1])
    url = url + last_day_of_month + date_obj.strftime("/%m/%Y") + URL5
    return url



if __name__ == "__main__":
    main()