from flask import request, jsonify, Blueprint
import json
# from ..dao.cities_dao import CityDAO
# from main.dao.routes_dao import RoutesDAO
from main.service.stop_times_service import StopTimesService
from main.service.graph2 import Graph, dijkstra, to_array
from main.service.graph import Graph2, dijkstra2, Node
from main.service.stops_service import StopsService
from main.service.timetable_service import TimetableService
from main.service.trips_import_servie import TripsService
mpk = Blueprint("mpk", __name__)


@mpk.route('/')
@mpk.route('/home', methods=['GET'])
def home():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})


@mpk.route('/public_transport', methods=['GET'])
def public_transport():
    return json.dumps("OK"), 200


@mpk.route('/public_transport/city/<city_id>/routes', methods=['POST'])
def city_named(city_id):
    """
    endpoint displaying all the routes in the particular city
    :param city_id:
    :return: JSON object containing info about every route and number of them
    """
    city = CityDAO.get_city_by_id(city_id)
    all_routes = RoutesDAO.get_all_routes()
    # city = City.query.filter_by(city_name=city_name).first_or_404()
    data = []
    for route in all_routes:
        route.route_desc2 = route.route_desc.split('-')[0] + '"'
        data.append(
            {
                "route_id": route.route_id,
                "route_short_name": route.route_short_name,
                "route_desc": route.route_desc2,
                "city_name": city.city_name
            }
        )
    return jsonify(
        message=f"{len(data)} routes displayed for {city.city_name}.",
        category="success",
        data=data,
        status=200
    )


@mpk.route('/public_transport/cities', methods=['GET'])
def cities():
    """
    endpoint displaying all the cities from database
    :return: JSON object
    """
    all_cities = CityDAO.get_all_cities()
    data = []
    for city in all_cities:
        data.append(
            {
                "city_id": city.city_id,
                "city_name": city.city_name
            }
        )
    return jsonify(
        message=f"{len(data)} cities displayed.",
        category="success",
        data=data,
        status=200
    )


@mpk.route('/stops/<start_id>/<end_id>', methods=['POST'])
def stops(start_id, end_id):
    """
    Endpoint displaying all the trips that go
    directly from the chosen start stop_id
    to the chosen endpoint stop_id
    :return:
    """
    data = StopTimesService.search_direct(start_id, end_id)
    return jsonify(
        message=f"{len(data)} cities displayed.",
        category="success",
        data=data,
        status=200
    )


@mpk.route('/stops/timed')
def stops_with_time():
    """
    Endpoint displaying all the trips that go
    directly from the chosen start stop_id
    to the chosen endpoint stop_id
    with the hour and minute specified
    """
    start_id = 3144
    end_id = 4651
    hour = "11"
    minute = "44"
    data = StopTimesService.direct_with_time(start_id, end_id, hour, minute)
    return jsonify(
        message=f"{len(data)} cities displayed.",
        category="success",
        data=data,
        status=200
    )


def build_graph():
    g = Graph()
    nodes = StopsService.get_all_stops_id()
    for i in nodes:
        g.add_node(i[0])

    edges = TimetableService.get_all_from_db()
    for i in edges:
        travel_time = int(i.travel_time.minute)
        g.add_edge(i.from_stop_id, i.to_stop_id, i.departure_time, travel_time, i.trip_id)

    return g


def build_graph2():
    nodes = StopsService.get_all_stops_id()
    nodes_list = []
    for i in nodes:
        n = Node(i[0])
        nodes_list.append(n)
    g = Graph2(nodes_list)
    edges = TimetableService.get_all_from_db()
    for i in edges:
        travel_time = int(i.travel_time.minute)
        g.connect(i.from_stop_id, i.to_stop_id, i.trip_id, travel_time)

    return g


graph = build_graph()


@mpk.route('/dijkstra/<from_stop_name>/<to_stop_name>')
def dijkstra_p(from_stop_name, to_stop_name):
    g = graph
    from_stop_id, to_stop_id = StopsService.get_stop_id(from_stop_name, to_stop_name)
    dist, prev = dijkstra(g, from_stop_id[0])
    route, times = to_array(prev, to_stop_id[0], dist)
    route_w_names = StopsService.get_stop_name(route)
    # trips_w_names = TripsService.get_trip_names(trips)
    data = []
    for i in range(len(route)):
        data.append(str(route_w_names[i] + "  time: " + str(times[i]) ))
    return jsonify(
        message=f"{len(data)} stops to take displayed.",
        category="success",
        data=data,
        status=200)



