# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
################################################
@app.route('/')
def welcome():
# available API's
     return(
         f'available routes:<br/>'
         f'/api/v1.0/precipitation<br/>'
         f'/api/v1.0/stations<br/>'
         f'/api/v1.0/tobs<br/>'
         f'/api/v1.0/start<br/>'  
         f'/api/v1.0/start/end'

         )
if __name__ == '__main__':
    app.run(debug=True)
   

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation and date"""
    # Query all precipitation and date
    results_date = dt.date(2017,8,23) - dt.timedelta(days=366)
    results = session.query(Measurement.date, Measurement.prcp).filter(func.strftime(Measurement.date >= results_date)).order_by(Measurement.date).all()

    session.close()


       # Convert list into dictionary
    all_precepitation=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precepitation.append(precipitation_dict)

    return jsonify(all_precepitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).filter(Measurement.station==station_Measurment_join[0][0]).first()
    session.close()
    all_station=[]
    for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
    return jsonify(all_station)

