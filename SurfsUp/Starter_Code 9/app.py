# Import the dependencies.
import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine ("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect =True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def Hello():
    """Availble API routes."""
    return (
        f"Available Routes:<br/>"        
        f"/api/v1.0/precipitation<br/>"        
        f"/api/v1.0/stations<br/>"       
        f"/api/v1.0/tobs<br/>"        
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end(enter as YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    start_date_str = "2017-08-23"
    
    start_date = dt.datetime.strptime(start_date_str, "%Y-%m-%d")
    
    end_date = start_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= end_date, Measurement.date <= start_date).order_by(Measurement.date)
    
    precipitation_date_tobs = []
    
    for each_row in results:
        dt_dict = {}
        dt_dict['date'] = each_row.date
        dt_dict['tobs'] = each_row.tobs
        precipitation_date_tobs.append(dt_dict)
    
    return jsonify(precipitation_date_tobs)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.name).all()
    
    station_details = list(np.ravel(results))
    
    return jsonify(station_details)

    
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    last_date = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    
    last_date_str = str(last_date)
    last_date_str = re.sub("'|,","", last_date_str)
    last_date_obj = dt.datetime.strptime(last_date_str, '(%Y-%m-%d)')
    query_start_date = dt.date(last_date_obj.year, last_date_obj.month, last_date_obj.day) - dt.timedelta(days=365)
    
    
    q_station_list = (session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
    
    station_one = q_station_list[0][0]
    
    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= query_start_date).filter(Measurement.station == station_one).all())
    
    tobs_list = []
    for result in results:
        line = {}
        line["Date"] = result[1]
        line["Station"] = result[0]
        line["Temperature"] = int(result[2])
        tobs_list.append(line)
        
    return jsonify(tobs_list)

    
    
@app.route("/api/v1.0/start")
def start():
   
    session = Session(engine)
    
    start_date = "2016-08-23"
    
    
    results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
        
    start_tobs = [{"Start_date": start_date, "max":max_temp, "average":avg_temp, "max":max_temp} for min_temp, avg_temp, max_temp in results]
        
    return jsonify(start_tobs)

@app.route("/api/v1.0/start/end")
def start_end():
    session = Session(engine)
    
    start_date = "2016-08-23"
    
    end_date = "2017-08-23"
    
    
    results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs)).filter(Measurement.date <= end_date).filter(Measurement.date >= start_date).all()
        
    start_tobs = [{"Start_date": start_date, "max":max_temp, "average":avg_temp, "max":max_temp} for min_temp, avg_temp, max_temp in results]
        
    return jsonify(start_tobs)
    
    
if __name__ == '__main__':
    app.run(debug=True)

                            
        
                                         


                                                                                               
                                                                                               
                                                                                             
        
       
  
  
    
        
        
        
        
        
        
        