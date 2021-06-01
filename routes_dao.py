from main.model.route import Routes
from . import engine


class RoutesDAO:

    @staticmethod
    def get_all_routes():
        """
        :return: all the Routes objects from db
        """
        return Routes.query.all()

    @staticmethod
    def get_routes_for_city(city_id):
        """
        :param city_id:
        :return: list[] of all the Routes objects where city_id
        """
        return Routes.query.fcilter_by(city_id=city_id).all()

    @staticmethod
    def import_dao(df):
        """
        This saves pandas df to database
        """
        df.to_sql('route2', engine, if_exists='replace', index=False)