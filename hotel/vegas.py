from bs4 import BeautifulSoup
import requests
import datetime
from selenium import webdriver
import sys

import urllib

PHANTOMJS_PATH = "/Users/carchi/bin/phantomjs-2.1.1-macosx"

def main():
    today = datetime.date.today()
    tomarrow = today + datetime.timedelta(days=1)
    guests = 2

    #browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    driver = webdriver.Chrome()
    params = {"arrive": today, "depart": tomarrow, "numGuest": guests}
    driver.get('https://www.mgmgrand.com/en/booking/room-booking.html')


    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.find("div", {"id": "rate-calendar-months-wrapper"})
    days = results.findAll("td", {"class": "date-wrapper"})
    my_data = []

    for day in days:
        data_date = day.attrs["data-date"]
        data_month = day.attrs["data-month"]
        data_year = day.attrs["data-year"]
        if not data_date:
            continue
        rate = day.find("span", {"class": "date-rate"})
        if not rate:
            continue
        rate = int(rate.text.split("$")[1])
        date = data_month + "/" + data_date + "/" + data_year
        my_data.append({"date": date, "price": rate})
    my_data.sort(key=lambda x: x["price"])
    for data in my_data:
        print(data["date"] + ": $" + str(data["price"]))



    print(len(days))


if __name__ == "__main__":
    main()