from ..app import db


class StopTimes(db.Model):
    __tablename__ = "stoptimes"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    trip_id = db.Column(db.String(20), db.ForeignKey("trips.trip_id"))
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    stop_id = db.Column(db.Integer)
    stop_sequence = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.trip_id}, {self.arrival_time}, {self.departure_time}, {self.stop_id}"
