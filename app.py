import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

# Save reference to the tables
measurement = Base.classes.measurement
station= Base.classes.station

session= Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the welcome route
@app.route("/")

# Add the routing information for each of the other routes
def welcome():
	return(
	'''
	Welcome to the Climate Analysis API!
	Available Routes:
	/api/v1.0/precipitation
	/api/v1.0/stations
	/api/v1.0/tobs
	/api/v1.0/temp/start/end
	''')

# -----------------------------
# 5. PRECIPITATION ROUTE
# -----------------------------

# Create precipitation route
@app.route("/api/v1.0/precipitation")



# Create the precipitation() function
def precipitation():
    
	# session= Session(engine)

	# Calculate the date one year ago from the most recent date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query: get date and precipitation for prev_year
    result= session.query(measurement.date, measurement.prcp).\
        filter(measurement.date>=prev_year).all()
		
	# Create dictionary w/ jsonify()--format results into .JSON
    precip = {date: prcp for date, prcp in result}
    return jsonify(precip)

# -----------------------------
# 6. STATIONS ROUTE
# -----------------------------

@app.route("/api/v1.0/stations")

def stations():
    
	# session= Session(engine)
    
    results = session.query(station.station).all()
	# Unravel results into one-dimensional array with:
		# `function np.ravel()`, `parameter = results`
	# Convert results array into a list with `list()`
    stations = list(np.ravel(results))
    return jsonify(stations=stations) 

# NOTE: `stations=stations` formats the list into JSON
# NOTE: Flask documentation: https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify

# -----------------------------
# 7. MONTHLY TEMPERATURE ROUTE
# -----------------------------

@app.route("/api/v1.0/tobs")

def temp_monthly():
    
	# session= Session(engine)
        
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
		filter(measurement.station == 'USC00519281').\
		filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# -----------------------------
# 8. STATISTICS ROUTE
# -----------------------------

# Provide both start and end date routes:
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

# Add parameters to `stats()`: `start` and `end` parameters
# def stats(start=dt.datetime(2017,1,1), end=dt.datetime(2017,2,28)):

 	# Query: min, avg, max temps; create list called `sel`
    # sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

	# Add `if-not` statement to determine start/end date
    # if not end:
	#     results = session.query(*sel).\
	# 	    filter(measurement.date >= start).\
	# 	    filter(measurement.date <= end).all()
	# temps = list(results)
    # return jsonify(temps=temps)
def get_temps(start, end=None):
    
	# session= Session(engine)
    
    sel = [measurement.date, measurement.tobs]
    if end:
        results = session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    else:
        results = session.query(*sel).filter(measurement.date == start).all()
    temps = [{"date": row[0], "temperature": row[1]} for row in results]
    return jsonify(temps)

# 		# NOTE: (*sel) - asterik indicates multiple results from query: minimum, average, and maximum temperatures


if __name__ == "__main__":
    app.run(debug=True)
