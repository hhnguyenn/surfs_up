#Add dependencies
import datetime as dt           
import numpy as np     
import pandas as pd    

#Add sqlalchemy dependencies 
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session      
from sqlalchemy import create_engine, func

#add code to import dependencies from Flask
from flask import Flask, jsonify

#Access SQLite database
engine=create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes
Base=automap_base()
Base.prepare(engine, reflect=True)

#Safe references to each table with variable
Measurement=Base.classes.measurement
Station=Base.classes.station    

#Create session link from Python to database
session = Session(engine)

#Set up Flask
#Create Flask application called "app"
app=Flask(__name__)

#create welcome route
@app.route("/")
#create function for routing information
def welcome():
    return(
    #add precipitation, stations, tobs, and temp routes
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#add another route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #write code that calculates date one year ago from recent
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    #write query to get date and precipitation for previous year
    #.\ means to continue code to next line
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

#add station route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)

#route to return temperature observations for prev year
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >=prev_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)
    
#route for summary statistics report
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results=session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        session.close()
        temps=list(np.ravel(results))
        return jsonify(temps)

    results=session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps=list(np.ravel(results))
    return jsonify(temps)





