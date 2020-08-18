#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *
#create_engine, func

import numpy as np
import pandas as pd

from flask import Flask, jsonify


# In[3]:


"""
Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
Use Flask to create your routes.

Routes:
/
    -Home page.
    -List all routes that are available.
"""
from flask import Flask, jsonify

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
        f"/api/v1.0/tobs<br/>"
#        f"/api/v1.0/<start>"
#        f"/api/v1.0/<start>/<end>"
        
    )


# In[4]:


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


# In[5]:


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


# In[6]:


"""
/api/v1.0/tobs
    -Query the dates and temperature observations of the most active station for the last year of data.
    -Return a JSON list of temperature observations (TOBS) for the previous year.
"""
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs=session.query(Measurement.station,Measurement.date, Measurement.tobs).    filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    return jsonify(tobs)


# In[7]:


if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




