from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Hotel, Price, Flight
import sys

app = Flask(__name__)

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    """
    Currently just list all the hotels that we have data base
    :return:
    """
    hotels = session.query(Hotel).order_by(Hotel.name)
    return render_template('index.html', hotels=hotels)

@app.route('/hotel/<month>/<days>')
def show_hotel_cheepest_for_days(month, days):
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
    return render_template('results.html', data=data)

@app.route('/<airport>/<month>/<days>')
def show_cheapest_for_days(airport, month, days):
    hotels = session.query(Hotel).order_by(Hotel.name)
    data = []
    #probably a way better way to do this, but just put something together quickly.
    for hotel in hotels:
        print(hotel.name)
        low_date = 0
        high_date = int(days)
        #this get us all the price for a specific month
        month_prices = session.query(Price).filter_by(hotel=hotel).filter(
            (sqlalchemy.extract('month', Price.date) == month)).order_by(Price.date)
        while month_prices.count() > high_date:
            cost = 0
            for price in range(low_date, high_date):
                cost += month_prices[price].price
            to_flights = session.query(Flight).filter_by(start_searched_airport=airport).filter(func.date(Flight.departure_time) == month_prices[low_date].date)
            from_flight = session.query(Flight).filter_by(end_searched_airport=airport).filter(func.date(Flight.departure_time) == month_prices[low_date].date)
            flight_data = _return_flight_data(to_flights, from_flight)
            data.append({"start": str(month_prices[low_date].date),
                         "end": str(month_prices[high_date].date),
                         "price": int(cost) + flight_data[0][3] + flight_data[1][3],
                         "hotel": month_prices[high_date].hotel.name,
                         "start_airport": flight_data[0][0],
                         "arival_time": flight_data[0][1],
                         "depature_time": flight_data[0][2],
                         "airline": flight_data[0][4],
                         "f_start_airport": flight_data[1][0],
                         "f_arival_time": flight_data[1][1],
                         "f_depature_time": flight_data[1][2],
                         "f_airline": flight_data[1][4]}
            )
            low_date += 1
            high_date += 1
    data.sort(key=lambda x: x["price"])
    print(data)
    return render_template('results.html', data=data)

def _return_flight_data(to_flight, from_flights):
    to_date = _format_flight_data(to_flight)
    from_date = _format_flight_data(from_flights)
    return [to_date, from_date]

def _format_flight_data(flights):
    if flights.count() > 0:
        s_port = flights[0].start_ariport + " -> " + flights[0].end_airport
        a_time = flights[0].departure_time
        arival_time = a_time.strftime("%H:%M:%S")
        d_time = flights[0].arrival_time
        depature_time = d_time.strftime("%H:%M:%S")
        a_price = int(flights[0].price)
        airline = flights[0].airline
    else:
        s_port = "NA"
        a_price = 2000
        arival_time = "NA"
        depature_time = "NA"
        airline = "NA"
    return s_port, arival_time, depature_time, a_price, airline

#this is just a copy of the above function with out months
@app.route('/all/<days>')
def show_all_data(days):
    """
    Show the cheapest price for all data in the database
    :param days: the number of days you want to stay in vegas
    :return: A webpage order by the cheapest rate
    """
    hotels = session.query(Hotel).order_by(Hotel.name)
    data = []
    for hotel in hotels:
        low_date = 0
        high_date = int(days)
        #this get us all the price for a specific month
        month_prices = session.query(Price).filter_by(hotel = hotel).order_by(Price.date)
        while month_prices.count() > high_date:
            cost = 0
            for price in range(low_date, high_date):
                cost += month_prices[price].price
            data.append({"start": str(month_prices[low_date].date), "end": str(month_prices[high_date].date), "price": int(cost), "hotel": month_prices[high_date].hotel.name})
            low_date += 1
            high_date += 1
    data.sort(key=lambda x: x["price"])
    return render_template('results.html', data=data)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5001)