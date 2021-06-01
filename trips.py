from ..app import db
from .stop_times import StopTimes


class Trips(db.Model):
    __tablename__ = "trips"

    route_id = db.Column(db.String(20))
    trip_id = db.Column(db.String(20), nullable=False, primary_key=True)
    trip_headsign = db.Column(db.Text)
    variant_id = db.Column(db.Integer)
    stop_times = db.relationship('StopTimes', backref='trips', lazy='dynamic')

    def __repr__(self):
        return f"{self.route_id}, {self.trip_id}, {self.trip_headsign}, {self.variant_id}"
