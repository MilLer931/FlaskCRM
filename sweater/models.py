from flask_login import UserMixin

from sweater import db, manager


class Authorization(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Authorization %r' % self.id  #Когда будем выбирать какой-либо объект на основе этого класса. Будет выдаваться сам объект и его айди


@manager.user_loader
def load_user(user_id):
    return Authorization.query.get(user_id)