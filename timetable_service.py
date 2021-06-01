from main.dao.timetable_dao import TimetableDAO


class TimetableService:

    @staticmethod
    def create_service():
        TimetableDAO.create()

    @staticmethod
    def get_all_from_db():
        return TimetableDAO.get_all()
