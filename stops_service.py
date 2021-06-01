import pandas as pd
from main.dao.stops_dao import StopsDAO


class StopsService:

    @staticmethod
    def stops_import_s():
        """ Handles the service of pandas import and calls the DAO"""
        path_to_file = 'data/stops.txt'
        df = pd.read_csv(path_to_file, usecols=['stop_id', 'stop_name'])
        StopsDAO.import_dao(df=df)
        return df

    @staticmethod
    def get_all_stops_id():
        result = StopsDAO.get_all_ids()
        return result

    @staticmethod
    def get_stop_id(from_stop_name, to_stop_name):
        from_stop_id = StopsDAO.get_stop_id(from_stop_name)
        to_stop_id = StopsDAO.get_stop_id(to_stop_name)
        return from_stop_id, to_stop_id

    @staticmethod
    def get_stop_name(route_list):
        stops_names = []
        for stop in route_list:
            temp = StopsDAO.get_stop_name(stop)
            stops_names.append(temp[0])
        return stops_names
