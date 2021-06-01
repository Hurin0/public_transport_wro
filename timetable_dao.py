from main.model.timetable import Timetable
from . import engine, session
from main.dao.stop_times_dao import StopTimesDAO
from datetime import time, datetime, date, timedelta


class TimetableDAO:

    @staticmethod
    def create():
        all_stoptimes = StopTimesDAO.get_all_selection()
        for row in range(len(all_stoptimes) - 1):
            if all_stoptimes[row][0] == all_stoptimes[row+1][0]:
                trip_id, departure_time, from_stop_id = all_stoptimes[row]
                _, arrival_time, to_stop_id = all_stoptimes[row+1]

                travel_time = (datetime.combine(date.today(), arrival_time)
                               - timedelta(hours=departure_time.hour, minutes=departure_time.minute)).time()

                Tt = Timetable(from_stop_id=from_stop_id, to_stop_id=to_stop_id, departure_time=departure_time,
                               travel_time=travel_time, trip_id=trip_id)

                session.add(Tt)
        session.commit()
        session.close()

    @staticmethod
    def get_all():
        return Timetable.query.all()
