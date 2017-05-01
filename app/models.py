from datetime import datetime
from extensions import db


class ParseTaskInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(155), unique=True)
    filename = db.Column(db.String(200))
    state = db.Column(db.String(30))
    weight = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    date_add = db.Column(db.DateTime, default=datetime.now)
