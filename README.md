# Vacation-Scraper-2
[![Quality Gate](https://sonarcloud.io/api/badges/gate?key=carchi8py%3AVacation-Scraper-2)](https://sonarcloud.io/dashboard?id=carchi8py%3AVacation-Scraper-2)

This web scraper finds the cheapest hotel prices in Vegas

## Prerequisites
### Python 3

```
pip3 install bs4
pip3 install flask
pip3 install sqlalchemy
pip3 install selenium
```

### Chrome Drivers
You'll need Chrome Drivers installed somewhere or Selenium will fail.
just follow this stack overflow page https://stackoverflow.com/questions/13724778/how-to-run-selenium-webdriver-test-cases-in-chrome

## Getting started
First run the database script to create a sqlite db to store the data in
```
python3 database_setup.py
```
Next run the vegas script, this will scrape each of the supported hotels. While this is running chrome
will open in the background.
```
python3 hotel/vegas.py
```
Last run the webpage scrip
```
python3 webpage.py
```