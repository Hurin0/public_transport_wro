from . import engine
from main.model.stops import Stops
from . import session


class StopsDAO:

    @staticmethod
    def import_dao(df):
        """ Saves pandas df to the database"""
        df.to_sql('stops', engine, if_exists='replace', index=False)

    @staticmethod
    def get_all():
        return Stops.query.all()

    @staticmethod
    def get_all_ids():
        return session.query(Stops.stop_id).all()

    @staticmethod
    def get_stop_name(stop_id):
        return session.query(Stops.stop_name).filter(Stops.stop_id == stop_id).first()

    @staticmethod
    def get_stop_id(stop_name):
        return session.query(Stops.stop_id).filter(Stops.stop_name == stop_name).first()
