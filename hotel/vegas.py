from bs4 import BeautifulSoup
from selenium import webdriver
import sys, os, inspect
import time
import datetime

#import the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from database_setup import Base, Hotel, Price

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

hotels = ["mandalaybay",
          "delanolasvegas",
          "luxor",
          "excalibur",
          "newyorknewyork",
          "montecarlo",
          "aria",
          "vdara",
          "bellagio",
          "mirage",
          "circuscircus",
          "mgmgrand",
          "signaturemgmgrand"]

def main():
    my_data = []
    for hotel in hotels:
        add_hotel_to_db(hotel)
        request = get_website(hotel)
        print(hotel)
        days = parse_data(request)
        my_data = get_prices(days, my_data, hotel)
    my_data.sort(key=lambda x: x["price"])
    for price in my_data:
        print(price["date"] + ": $" + str(price["price"]) + " at " + price["hotel"])

def add_hotel_to_db(hotel):
    new_hotel = Hotel(name = hotel)
    session.add(new_hotel)
    session.commit()

def add_price_to_db(date, rate, hotel):
    hotel_obj = session.query(Hotel).filter_by(name=hotel).one()
    date_obj = datetime.datetime.strptime(date, "%m/%d/%Y").date()
    new_price = Price(hotel = hotel_obj, date = date_obj, price = rate)
    session.add(new_price)
    session.commit()

def parse_data(request):
    soup = BeautifulSoup(request.page_source, "html.parser")
    results = soup.find("div", {"id": "rate-calendar-months-wrapper"})
    days = results.findAll("td", {"class": "date-wrapper"})
    return days

def get_prices(days, my_data, hotel):

    for day in days:
        data_date = day.attrs["data-date"]
        data_month = str(int(day.attrs["data-month"]) + 1)
        data_year = day.attrs["data-year"]
        if not data_date:
            continue
        rate = day.find("span", {"class": "date-rate"})
        if not rate:
            continue
        rate = int(rate.text.split("$")[1])
        date = data_month + "/" + data_date + "/" + data_year
        my_data.append({"date": date, "price": rate, "hotel": hotel})
        add_price_to_db(date, rate, hotel)
    return my_data

def get_website(hotel):
    """
    Load a website in Chrome and return the html (after java script has loaded
    :param url: the url to load
    :return: the urls html
    """
    url = format_url(hotel)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    return driver

def format_url(url):
    return "https://www." + url + ".com/en/booking/room-booking.html"

if __name__ == "__main__":
    main()