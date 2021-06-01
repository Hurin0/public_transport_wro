import pandas as pd
from main.dao.trips_dao import TripsDAO


class TripsService:

    @staticmethod
    def trips_import_s():
        """Handles the service of pandas import and calls the DAO"""
        path_to_file = 'data/trips.txt'
        df = pd.read_csv(path_to_file, usecols=['route_id', 'trip_id', 'trip_headsign', 'variant_id'])
        TripsDAO.import_dao(df=df)
        return df

    @staticmethod
    def create_list_of_all_trip_id():
        all_trip_id = []
        all_trips = TripsDAO.get_all_trips()
        for trip in all_trips:
            all_trip_id.append(trip.trip_id)
        return all_trip_id

    @staticmethod
    def get_trip_names(trips_list):
        trips_names = []
        for trip in trips_list:
            temp1, temp2 = TripsDAO.get_trip_name(trip)
            trips_names.append(temp1 + "  " + temp2)
        return trips_names

