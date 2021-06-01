import pandas as pd
from ..dao.routes_dao import RoutesDAO


class RouteService:

    @staticmethod
    def route_import():
        """ Handles the service of saving df to database
            calls the DAO. Returns the df"""
        path_to_file = 'data/routes.csv'
        df = pd.read_csv(path_to_file, usecols=['route_id', 'route_short_name', 'route_desc'])
        df['city_id'] = 1
        RoutesDAO.import_dao(df=df)
        return df
