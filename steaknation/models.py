from steaknation import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_phone_number):
    return User.query.get(user_phone_number)


class User(db.Model, UserMixin):
    fullname = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), primary_key=True, nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(60), nullable=False)
    reservations = db.Relationship('Reservation', backref='user', lazy=True)

    def __repr__(self):
        return f"{self.fullname}\t{self.phone_number}"

    def get_id(self):
        return self.phone_number


class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    datetime = db.Column(db.DateTime, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user_phone = db.Column(db.String(10), db.ForeignKey('user.phone_number'), nullable=False)

    def __repr__(self):
        return f"{self.name}: {self.phone_number}\nDate: {self.date}, {self.time}"

