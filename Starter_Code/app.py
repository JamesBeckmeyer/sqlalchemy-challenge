# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
#session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return (
        f"/api/v1.0/precipitation will take you to percipitation analysis dictionary<br/>"
        f"/api/v1.0/stations will take you to a JSON list of stations<br/>"
        f"/api/v1.0/tobs will take you to a JSON list of temperatures from the most active station for the most recent year br/>"
        f"/api/v1.0/<start> will take your <start> date input and calculate min, max and average temperatures from then to the most recent date<br/>"
        f"/api/v1.0/<start>/<end> will take your <start> date input and calculate min, max and average temperatures from <start> to <end> <br/>"
        f"dates in YYYY-MM-DD format"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    data = session.query(measurement.prcp, measurement.date).\
    filter(measurement.date >= '2016-08-23').\
    order_by(measurement.date).all()
    session.close()
    df = pd.DataFrame(data)
    
    results = df.set_index('date').T.to_dict('list')

    return results

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    temps = session.query(measurement.tobs).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281').\
        order_by(measurement.tobs.desc()).all() 
    session.close()
    return jsonify(temps)
    

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    min_temp = session.query(measurement.tobs).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').order_by(measurement.tobs).first()
    max_temp = session.query(measurement.tobs).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').order_by(measurement.tobs.desc()).first()
    avg_temp = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').all()
    temp_list = [min_temp, max_temp, avg_temp]
    session.close()
    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    min_temp2 = session.query(measurement.tobs).filter(measurement.date <= end).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').order_by(measurement.tobs).first()
    max_temp2 = session.query(measurement.tobs).filter(measurement.date <= end).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').order_by(measurement.tobs.desc()).first()
    avg_temp2 = session.query(func.avg(measurement.tobs)).filter(measurement.date <= end).filter(measurement.date >= start).filter(measurement.station == 'USC00519281').all()
    temp_list2 = [min_temp2, max_temp2, avg_temp2]
    session.close()
    return jsonify(temp_list2)


if __name__ == "__main__":
    app.run(debug=True)