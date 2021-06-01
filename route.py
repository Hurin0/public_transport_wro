from ..app import db


class Routes(db.Model):
    __tablename__ = 'route2'

    route_id = db.Column(db.String(20), nullable=False, primary_key=True)
    route_short_name = db.Column(db.String(20))
    route_desc = db.Column(db.Text)
    city_id = db.Column(db.Integer, db.ForeignKey("cities1.city_id"))

    def __repr__(self):
        return f"{self.route_id}, {self.route_short_name}, {self.route_desc}"
