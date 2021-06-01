from ..app import db


class City(db.Model):
    __tablename__ = "cities1"

    city_id = db.Column(db.Integer, nullable=False, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False, unique=True)
    routes = db.relationship('Routes', backref='city', lazy='dynamic')

    def __repr__(self):
        return f"{self.city_id}, {self.city_name}"

