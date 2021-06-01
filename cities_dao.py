from main.model.cities import City


class CityDAO:

    @staticmethod
    def get_all_cities():
        """
        Returns all the City model objects from database
        """
        return City.query.all()

    @staticmethod
    def get_city_by_id(city_id):
        """
        Returns the City object where city_id matches
        :param city_id:
        """
        return City.query.filter_by(city_id=city_id).first()

    @staticmethod
    def get_by_cityname(city_name):
        """
        Returns the City object where city_name matches
        :param city_name:
        """
        return City.query.filter(city_name=city_name).first()
