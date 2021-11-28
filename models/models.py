from service import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return user


class Project(db.Model):
    project_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(length=30), nullable=False, unique=True)
    fulfilment = db.Column(db.Integer(), default=0)
    project_started = db.Column(db.Date, nullable=False)
    project_deadline = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Project: {self.project_name}, accomplished: {self.fulfilment}, deadline: {self.project_deadline}"


class Task(db.Model):
    task_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(length=30))
    task_name = db.Column(db.String(length=30), nullable=False, unique=True)
    task_fulfilment = db.Column(db.Integer(), default=0)
    task_started = db.Column(db.Date, nullable=False)
    task_deadline = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Project: {self.project_name}, task: {self.task_name}, accomplished: {self.task_fulfilment}, deadline: {self.task_deadline}"


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(length=30), default="Developer")
    salary = db.Column(db.Integer(), nullable=False, default=500)
    bonus = db.Column(db.Integer(), nullable=False, default=0)
    task_name = db.Column(db.String(length=30), default="Training")
    project_name = db.Column(db.String(length=30), default="Bench")

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"Username: {self.username}, role: {self.role}"
