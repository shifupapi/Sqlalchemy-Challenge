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

   

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation and date"""
    # Query all precipitation and date
    results_date = dt.date(2017,8,23) - dt.timedelta(days=366)
    results = session.query(Measurement.date, Measurement.prcp).filter(func.strftime(Measurement.date >= results_date)).order_by(Measurement.date).all()
    prcp2={date: prcp for date, prcp in results}

    session.close()
    return jsonify(prcp2)



@app.route("/api/v1.0/stations")
def stations():

    # Query all stations
    results = session.query(Station.station).all()
    all_stations=list(np.ravel(results))
    session.close()
    return jsonify(all_stations)
    

@app.route("/api/v1.0/tobs")
def tempartureobs():
    #results_date = dt.date(2017,8,23) - dt.timedelta(days=366)

    station_Measurment_join=session.query(Measurement.station,func.count(Measurement.station)).\
                       group_by(Measurement.station).\
                       order_by(func.count(Measurement.station).desc()).all()
    temp=session.query(Measurement.date).order_by(Measurement.date.desc()).\
             filter(Measurement.station==station_Measurment_join[0][0]).first()
    str_date=list(np.ravel(temp))[0]
    latest_date=dt.datetime.strptime(str_date,"%Y-%m-%d")
    year_back=latest_date-dt.timedelta(days=366)

    results_temp=session.query(Measurement.tobs).\
             filter(Measurement.station==station_Measurment_join[0][0]).\
             filter(Measurement.date>=year_back).all()

    session.close()
    return jsonify(results_temp)
    

# # Perform a query to retrieve the data and precipitation scores
#     results=session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
#             filter(Measurement.date>=year_back).all()
#     session.close()
#     all_temperature=[]
#     for tobs,date in results:
#         tobs_dict={}
#         tobs_dict['date']=date
#         tobs_dict['tobs']=tobs
#         all_temperature.append(tobs_dict)
#     return jsonify(all_temperature)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
    results_temp=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
             filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    temp=list(np.ravel(results_temp))

    session.close()
    return jsonify(temp)
    
    results_temp=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
             filter(Measurement.date>=start).all()
    temp=list(np.ravel(results_temp))

    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    
#     results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#                 filter(Measurement.date >= start).filter(Measurement.date <= end).all()
#     session.close()
#     temp_obs={}
#     temp_obs["Min_Temp"]=results[0][0]
#     temp_obs["avg_Temp"]=results[0][1]
#     temp_obs["max_Temp"]=results[0][2]
#     return jsonify(temp_obs)

if __name__ == '__main__':
    app.run(debug=True)
