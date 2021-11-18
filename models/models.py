from service import db


class Project:
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(length=30), nullable=False, unique=True)
    fulfilment = db.Column(db.Integer())
    project_started = db.Column(db.DateTime, nullable=False)
    project_deadline = db.Column(db.DateTime, nullable=False)
    currently_paid = db.Column(db.Integer(), nullable=False, default=0)
    predicted_project_salary = db.Column(db.Integer(), nullable=False, default=0)
    expected_project_salary = db.Column(db.Integer(), nullable=False, default=0)


class Task:
    project_name = db.Column(db.String(length=30), db.ForeignKey('user.id'))
    task_name = db.Column(db.String(length=30), nullable=False, unique=True)
    teamlead = db.relationship('User', backref='task', lazy=True)
    task_fulfilment = db.Column(db.Integer())
    task_started = db.Column(db.DateTime, nullable=False)
    task_deadline = db.Column(db.DateTime, nullable=False)
    currently_paid = db.Column(db.Integer(), nullable=False, default=0)
    predicted_task_salary = db.Column(db.Integer(), nullable=False, default=0)
    expected_task_salary = db.Column(db.Integer(), nullable=False, default=0)
    # Need to add perfomers and their role


class User:
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(length=30), nullable=False, unique=True)
    salary = db.Column(db.Integer(), nullable=False, default=500)
    bonus = db.Column(db.Integer(), nullable=False, default=0)
    task_name = db.Column(db.Integer(), db.ForeignKey('task.task_name'))
    project_name = db.Column(db.Integer(), db.ForeignKey('project.project_name'))
