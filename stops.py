from ..app import db


class Stops(db.Model):
    __tablename__ = "stops"

    stop_id = db.Column(db.Integer, nullable=False, primary_key=True)
    stop_name = db.Column(db.Text)


    def __repr__(self):
        return f"{self.stop_id}, {self.stop_name}"
