##########################
# IMPORTING DEPENDENCIES #
##########################
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

##################
# DATABASE SETUP #
##################
# Creating engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflecting the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Opening Session
session.Session(engine)

###############
# FLASK SETUP #
###############
app = Flask(__name__)

#################################################
# CALCULATING THE TMIN, TAVG, AND TMAX FOR YOUR #
# TRIP USING THE PREVIOUS YEAR'S DATA FOR THOSE #
# SAME DATES.                                   #
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

#############################################
# SETTING UP FLASK ROUTES AVAILABLE TO USER #
#############################################
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

################################
# CREATING PRECIPITATION ROUTE #
################################
@app.route("/api/v1.0/names")
def precipitation():
"""Query the dates and temperature observations of the most active station for \
the last year of data. Return a JSON list of temperature observations (TOBS)\
for the previous year."""

    latest_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.
    date))).all()
    max_date_string = latest_date[0][0]
    max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")

    # Initializing beginning of search query
    start_date = max_date - datetime.timedelta(366)

    # Querying dates and precipitation data
    precipitation_data = session.query(func.strftime("%Y-%m-%d",
    Measurement.date), Measurement.prcp).filter(func.strftime("%Y-%m-%d",
    Measurement.date) >= begin_date).all()

    # Initilizing a dictionary with the date (as the key) and the precipitation
    # value as the value.
    results_query_dict = {}
    for result in precipitation_data:
        results_query_dict[result[0]] = result[1]

    return jsonify(results_dict)

###########################
# CREATING STATIONS ROUTE #
###########################
@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of all available stations for the user to query"""

    # query stations list
    stations_data = session.query(Station).all()

    # creating a dictionary to store returned query information
    stations_list = []
    for station in stations_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)
    return jsonify(stations_list)

###############################################
# CREATING TEMPERATURE OBSERVATION DATA ROUTE #
###############################################
@app.route("/api/v1.0/tobs")
    ""Query the dates and temperature observations of the most active station \
    for the last year of data. Return a JSON list of temperature observations \
    (TOBS) for the previous year."""

# Identifying the latest date in our SQL database
    latest_date_query = session.query(func.max(func.strftime("%Y-%m-%d",
    Measurement.date))).all()

    max_date_string = latest_date[0][0]

    max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")

    # Setting date at beginning of Query
    start_date = max_date - datetime.timedelta(365)

    # Returning temperatire recording for last year
    last_year_results = session.query(Measurement).filter(func.strftime("%Y-%m-%d",
    Measurement.date) >= begin_date).all()

    # Dictionary and for loop to iterate through and store observations.
    TOBS_list = []
    for result in last_year_results
        TOBS_dict = {}
        TOBS_dict["date"] = result.dates
        TOBS_dict["station"] = results.station
        TOBS_dict["tobs"] = results.tobs
        TOBS_list.append(TOBS_dict)

    return jsonify(TOBS_list)

@app.route("/api/v1.0/<start>/<end>")

"""Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
