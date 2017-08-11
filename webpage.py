from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Hotel, Price
import sys

app = Flask(__name__)

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    hotels = session.query(Hotel).order_by(Hotel.name)
    return render_template('index.html', hotels=hotels)

@app.route('/cheepest/<month>/<days>')
def show_cheepest_for_days(month, days):
    hotels = session.query(Hotel).order_by(Hotel.name)
    data = []
    for hotel in hotels:
        low_date = 0
        high_date = int(days)
        #this get us all the price for a specific month
        month_prices = session.query(Price).filter_by(hotel = hotel).filter((sqlalchemy.extract('month', Price.date) == month)).order_by(Price.date)
        while month_prices.count() > high_date:
            cost = 0
            for price in range(low_date, high_date):
                cost += month_prices[price].price
            data.append({"start": str(month_prices[low_date].date), "end": str(month_prices[high_date].date), "price": int(cost), "hotel": month_prices[high_date].hotel.name})
            low_date += 1
            high_date += 1
    data.sort(key=lambda x: x["price"])
    for each in data:
        print(each["start"] + " to " + each["end"]+ ": $" + str(each["price"]) + " at " + each["hotel"])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)