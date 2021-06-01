from ..app import db


class Timetable(db.Model):
    __tablename__ = "timetable"

    from_stop_id = db.Column(db.Integer, nullable=False)
    to_stop_id = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    travel_time = db.Column(db.Time, nullable=False)
    trip_id = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"{self.from_stop_id}, {self.to_stop_id}, {self.departure_time}," \
               f"{self.travel_time}, {self.trip_id}"
