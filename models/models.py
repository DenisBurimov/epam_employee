from service import db


class Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(length=30), nullable=False, unique=True)
    fulfilment = db.Column(db.Integer())
    project_started = db.Column(db.Date, nullable=False)
    project_deadline = db.Column(db.Date, nullable=False)
    currently_paid = db.Column(db.Integer(), nullable=False, default=0)
    predicted_project_salary = db.Column(db.Integer(), nullable=False, default=0)
    expected_project_salary = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f"Project: {self.project_name}, accomplished: {self.fulfilment}, deadline: {self.project_deadline}"


class Task(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(length=30), db.ForeignKey('project.project_name'))
    task_name = db.Column(db.String(length=30), nullable=False, unique=True)
    task_fulfilment = db.Column(db.Integer())
    task_started = db.Column(db.Date, nullable=False)
    task_deadline = db.Column(db.Date, nullable=False)
    currently_paid = db.Column(db.Integer(), nullable=False, default=0)
    predicted_task_salary = db.Column(db.Integer(), nullable=False, default=0)
    expected_task_salary = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f"Project: {self.project_name}, task: {self.task_name}, accomplished: {self.task_fulfilment}, deadline: {self.task_deadline}"


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(length=30))
    salary = db.Column(db.Integer(), nullable=False, default=500)
    bonus = db.Column(db.Integer(), nullable=False, default=0)
    task_name = db.Column(db.String(length=30), db.ForeignKey('task.task_name'))
    project_name = db.Column(db.String(length=30), db.ForeignKey('project.project_name'))

    def __repr__(self):
        return f"Username: {self.username}, role: {self.role}"
