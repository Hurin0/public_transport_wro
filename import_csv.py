from flask import request, jsonify, Blueprint
import psycopg2
from ..model.routes import Route
from ..service.trips_import_servie import TripsService
from ..service.route_service import RouteService
from ..service.stop_times_service import StopTimesService
from ..service.stops_service import StopsService
from main.service.timetable_service import TimetableService

from ..app import app

importer = Blueprint("importer", __name__)

db_conn = psycopg2.connect(host='localhost', port='9000', dbname='mpkweb', user='postgres', password='toor')
db_cursor = db_conn.cursor()
db_cursor.execute("ROLLBACK")
db_conn.commit()


@importer.route('/import_wroclaw')
def import_wroclaw():
    """
    Imports all the routes for city Wroclaw from csv file
    using the psycopg2 cursor and then saving it to the database
    """
    if request.method == 'GET':
        path_to_file = 'data/routes.csv'
        f_contents = open(path_to_file, 'r')
        headers = next(f_contents)

        db_cursor.copy_from(f_contents, 'routes', sep=",", columns=('route_id', 'agency_id', 'route_short_name',
                                                            'route_long_name', 'route_desc', 'route_type', 'route_type2_id',
                                                            'valid_from', 'valid_until'))
        db_cursor.execute(Route.import_wroclaw)
        db_cursor.close()
        db_conn.commit()
        db_conn.close()

        return jsonify({"response": "Routes imported"})


@importer.route('/import_cities')
def city_import():
    """
    Imports all the cities from csv file
    """
    if request.method == 'GET':
        path_to_file = 'data/cities.csv'
        f_contents = open(path_to_file, 'r')
        headers = next(f_contents)

        db_cursor.copy_from(f_contents, '"cities1"', sep=",", columns=('city_id', 'city_name'))

        db_cursor.close()
        db_conn.commit()
        db_conn.close()

        return jsonify({"response": "Cities imported"})


@importer.route('/pandas_import')
def pandas_import():
    """
    Imports all the routes from csv file using pandas
    """
    if request.method == 'GET':
        df = RouteService.route_import()
        return df.to_html(header='True', table_id='route2')

    return jsonify({"response": "It did not worked."})


@importer.route('/trips_import')
def trips_import():
    """
    Imports all the trips from csv file using pandas
    """
    if request.method == 'GET':
        df = TripsService.trips_import_s()
        return jsonify({"response": "It did worked."})

    return jsonify({"response": "It did not worked."})


@importer.route('/stop_times_import')
def stop_times_import():
    """
    Imports all the stoptimes from csv file using pandas
    """
    if request.method == 'GET':
        df = StopTimesService.st_import_fix_hours()
        return jsonify({"response": "It did worked."})
    return jsonify({"response": "It did not worked."})


@importer.route('/stops_import')
def stops_import():
    """
    Imports all the stops info from csv file using pandas
    """
    if request.method == 'GET':
        df = StopsService.stops_import_s()
        return jsonify({"response": "It did worked."})
    return jsonify({"response": "It did not worked."})


@importer.route('/timetable_create')
def timetable_create():

    if request.method == 'GET':
        TimetableService.create_service()
        return jsonify({"response": "It did worked."})
    return jsonify({"response": "It did not worked."})