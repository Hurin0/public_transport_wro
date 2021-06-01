from ..app import db


class Route(db.Model):
    __tablename__ = 'routes'

    route_id = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    agency_id = db.Column(db.Integer, unique=False)
    route_short_name = db.Column(db.String(20))
    route_long_name = db.Column(db.String(50), nullable=True)
    route_desc = db.Column(db.Text)
    route_type = db.Column(db.Integer)
    route_type2_id = db.Column(db.Integer)
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)
    city_id = db.Column(db.Integer, db.ForeignKey("cities1.city_id"))

    def __repr__(self):
        return f"{self.route_id}, {self.route_short_name}, {self.route_desc}"

    import_wroclaw = ("""
        UPDATE routes 
        SET city_id = 1 
        WHERE city_id IS NULL
        """)
