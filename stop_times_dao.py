from datetime import time, datetime, date, timedelta

from . import engine, session
from main.model.stop_times import StopTimes
from main.model.trips import Trips
from sqlalchemy import func


class StopTimesDAO:

    @staticmethod
    def import_dao(df):
        """ This saves pandas df to database """
        df.to_sql('stoptimes', engine, if_exists='append')

    @staticmethod
    def search_for_stop(stop_id):
        """
        :param stop_id:
        :return: list[] of all the StopTimes objects with given stop_id
        """
        return StopTimes.query.filter_by(stop_id=stop_id).all()

    @staticmethod
    def get_all_stops_for_trip(trip_id):
        """
        :param trip_id:
        :return: list[] of all the StopTimes objects with given trip_id
        """
        return StopTimes.query.filter_by(trip_id=trip_id).all()

    @staticmethod
    def get_all():
        """
        :return: all the StopTimes objects from database
        """
        return session.query(StopTimes).all()

    @staticmethod
    def get_all_selection():
        return session.query(StopTimes.trip_id, StopTimes.departure_time, StopTimes.stop_id).all()

    @staticmethod
    def order_by_trip(stop_id):
        trips = StopTimes.query.filter_by(stop_id=stop_id).order_by(StopTimes.trip_id).all()
        return trips

    @staticmethod
    def check_for_trip(trip_id):
        """
        Checks if there is trip with this id
        :param trip_id:
        :return: StopTimes object if there is one with this trip_id
        """
        return StopTimes.query.filter_by(trip_id=trip_id).first()

    @staticmethod
    def search_for_stop_time(stop_id, hour, minute, how_many_minutes):
        """
        Searches for all the StopTimes objects with stop_id (trips that reaches this stop)
        with given hour and minute at what to start search
        :param stop_id: ID of the stop (either start or end)
        :param hour: String - hour of your planning start of journey
        :param minute: String - minute of planning start of journey
        :param how_many_minutes: Int - number of minutes to the future to search for connections
        :return: list[]
        """
        given_time = time(int(hour), int(minute))
        search_time = (datetime.combine(date.today(), given_time) + timedelta(minutes=how_many_minutes)).time()

        return session.query(StopTimes).filter(StopTimes.stop_id == stop_id) \
            .filter((StopTimes.departure_time > given_time) & (StopTimes.departure_time < search_time)).all()

    @staticmethod
    def search_join_for_variants(stop_id, hour, minute, how_many_minutes):
        """
        Searches for all the StopTimes objects JOINED with Trips object
        with stop_id (trips that reaches this stop)
        with given hour and minute at what to start search
        :param stop_id: ID of the stop (either start or end)
        :param hour: String - hour of your planning start of journey
        :param minute: String - minute of planning start of journey
        :param how_many_minutes: Int - number of minutes to the future to search for connections
        :return: list of tuples [()]
        TODO - change return to list
        """
        given_time = time(int(hour), int(minute))
        search_time = (datetime.combine(date.today(), given_time) + timedelta(minutes=how_many_minutes)).time()
        return session.query(StopTimes, Trips.variant_id)\
            .filter(StopTimes.trip_id == Trips.trip_id)\
            .filter(StopTimes.stop_id == stop_id) \
            .filter((StopTimes.departure_time > given_time) & (StopTimes.departure_time < search_time)).all()

