from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return(
    "<h1>Hawaii Climate App (Flask API)</h1>"
    "<h3>Available Routes:</h3>"
    "/api/v1.0/precipitation<br/>"
    "<strong>Precipitation data</strong>"
    "<br/>"
    "<br/>"
    "/api/v1.0/stations<br/>"
    "<strong>Weather Stations</strong>"
    "<br/>"
    "<br/>"
    "/api/v1.0/tobs<br/>"
    "<strong>Observations</strong>"
    "<br/>"
    "<br/>"
    '/api/v1.0/"(start_date)"<br/>'
    "<strong>Infromation for all dates from the start date</strong>"
    "<br/>"
    "<br/>"
    '/api/v1.0/"(start_date)"/"(End_Date)"<br/>'
    "<strong>Infromation for a specific date range</strong>"
    "<br/>"
    "<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    precipitation_dict = list(np.ravel(precipitation_results))

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()

    station_dict = list(np.ravel(station_results))

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.tobs,Measurement.date).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()

            
    tobs_dict = list(np.ravel(tobs_results))
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        start_day_list = list(start_day)
        return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
        start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()       
        start_end_list = list(start_end)
        return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
