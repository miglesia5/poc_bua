from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from bua import db, login_manager

from flask_login import UserMixin


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



@login_manager.user_loader
def load_user(squad_id):
    return Squad.query.get(int(squad_id))


class Squad(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    squadname = db.Column(db.String(20), unique=True, nullable=False)
    squad_members=db.Column(db.String(3))
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String, default='user')
    tasks = db.relationship('Task', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['squad_id']
        except:
            return None
        return Squad.query.get(user_id)

    def __repr__(self):
        return f"{self.squad_members}"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    activity = db.Column(db.Text, nullable = False)
    tool = db.Column(db.String(20), nullable = False)
    product = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.Text, nullable=False)

    avg_time = db.Column(db.String(3), nullable = False)
    volume = db.Column(db.String(3), nullable = False)

    pain_point = db.Column(db.Text, nullable = False)
    pain_point_time = db.Column(db.String(3), nullable = False)

    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    squad_id = db.Column(db.Integer, db.ForeignKey('squad.id'), nullable = False)

    def __repr__(self):
        return f"Task('{self.squad}', '{self.date_posted}')"


# Create a model to show progress actions solutions and time save
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200))
    affected_volume = db.Column(db.String)
    saving = db.Column(db.String(4))
    complete = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)


    def __repr__(self):
        return f"Post('{self.goal}', '{self.date_posted}')"

admin = Admin()
admin.add_view(ModelView(Squad, db.session))