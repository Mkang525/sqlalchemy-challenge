import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *

import numpy as np
import pandas as pd

from flask import Flask, jsonify

"""
Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
Use Flask to create your routes.
"""

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():   
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"       
        f"Specific Dates- Format: YYYY-MM-DD</br>"
        f"/api/v1.0/<start></br>"
        
    )

"""
/api/v1.0/precipitation
    -Convert the query results to a dictionary using date as the key and prcp as the value.
    -Return the JSON representation of your dictionary.
"""
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)





"""
/api/v1.0/stations
    -Return a JSON list of stations from the dataset.
"""
Base = automap_base()
Base.prepare(engine, reflect=True)
Station= Base.classes.station

@app.route("/api/v1.0/stations")
def stations():    
    session = Session(engine)
    stations = session.query(Station.station,Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    all_stations = list(np.ravel(stations))

    return jsonify(stations)


"""
/api/v1.0/tobs
    -Query the dates and temperature observations of the most active station for the last year of data.
    -Return a JSON list of temperature observations (TOBS) for the previous year.
"""
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs=session.query(Measurement.station,Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    return jsonify(tobs)

"""
/api/v1.0/<start> 
    -Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start 
     or start-end range.
    -When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    -When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and 
     end date inclusive.

"""    
@app.route("/api/v1.0/<start>")

def your_route(start=None):

    session = Session(engine)
    
    start_list = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    tobs_list = []
    for a, b, c, d in start_list:
        tobs_dict = {}
        tobs_dict["Date"] = a
        tobs_dict["Min"] = b
        tobs_dict["Max"] = c
        tobs_dict["Avg"] = d
    
        tobs_list.append(tobs_dict)
        
    return jsonify(tobs_list)

            
@app.route("/api/v1.0/<start>/<end>")
def end_route(start=None,end=None):

    session = Session(engine)
    
    start_end_list = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >=start).\
        filter(Measurement.date<=end).\
        group_by(Measurement.date).all()
    
    tobs_se_list = []
    for a, b, c, d in start_end_list:
        tobs_se_dict = {}
        tobs_se_dict["Date"] = a
        tobs_se_dict["Min"] = b
        tobs_se_dict["Max"] = c
        tobs_se_dict["Avg"] = d
    
        tobs_se_list.append(tobs_se_dict)

    return jsonify(tobs_se_list)

        
if __name__ == "__main__":
    app.run(debug=True)  


    
  





            


