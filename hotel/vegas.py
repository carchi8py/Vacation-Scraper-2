from bs4 import BeautifulSoup
import requests
import datetime
from selenium import webdriver

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
    print(results)


if __name__ == "__main__":
    main()