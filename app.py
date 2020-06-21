#################################################
# IMPORTING DEPENDENCIES
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# DATABASE SETUP
#################################################
# Creating engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflecting the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Opening Session
session.Session(engine)

#################################################
# FLASK SETUP
#################################################
app = Flask(__name__)

#################################################
# CALCULATING THE TMIN, TAVG, AND TMAX FOR YOUR
# TRIP USING THE PREVIOUS YEAR'S DATA FOR THOSE
# SAME DATES.
#################################################
# This function called `calc_temps` will accept start date and end date in the
# format '%Y-%m-%d' and return the minimum, average, and maximum temperatures
# for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
     func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <=
        end_date).all()

# Setting Flask Routes
@app.route("/")
def welcome():
    """A list of all available API routes to the user"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"


@app.route("/api/v1.0/names")
def precipitation():
"""Query the dates and temperature observations of the most active station for \
the last year of data. Return a JSON list of temperature observations (TOBS)\
for the previous year."""

    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")
