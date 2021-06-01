from main.model.trips import Trips
from . import engine


class TripsDAO:

    @staticmethod
    def import_dao(df):
        """ Saves pandas df to the database """
        df.to_sql('trips', engine, if_exists='append', index=False)

    @staticmethod
    def get_trip_name(trip_id):
        """
        :param trip_id:
        :return: Headsign and Route_id of Trips objects with given ID
        """
        trip = Trips.query.filter_by(trip_id=trip_id).first()

        return trip.trip_headsign, trip.route_id

    # def get_trips_start(stop_id):
    #
    #     trip_with_startstop = Trips.query.filter_by(stop_times.stop_id=stop_id).all()
    #

    @staticmethod
    def get_all_trips():
        """ Returns all the Trips objects from database"""
        return Trips.query.all()
