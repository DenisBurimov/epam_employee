from service import db


class Project(db.Model):
    project_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(length=30), nullable=False, unique=True)
    fulfilment = db.Column(db.Integer(), default=0)
    project_started = db.Column(db.Date, nullable=False)
    project_deadline = db.Column(db.Date, nullable=False)
    currently_paid = db.Column(db.Integer(), nullable=False, default=0)
    predicted_project_salary = db.Column(db.Integer(), nullable=False, default=0)
    expected_project_salary = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f"Project: {self.project_name}, accomplished: {self.fulfilment}, deadline: {self.project_deadline}"


class Task(db.Model):
    task_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(length=30))
    task_name = db.Column(db.String(length=30), nullable=False, unique=True)
    task_fulfilment = db.Column(db.Integer(), default=0)
    task_started = db.Column(db.Date, nullable=False)
    task_deadline = db.Column(db.Date, nullable=False)
    # Add difference between today and deadline
    currently_paid = db.Column(db.Integer(), nullable=False, default=0) # Is timedifference * salaries sum
    predicted_task_salary = db.Column(db.Integer(), nullable=False, default=0) # Just put manually
    expected_task_salary = db.Column(db.Integer(), nullable=False, default=0) # Calculated as sum of salaries of those who is on this task pruducted with timedifference

    def __repr__(self):
        return f"Project: {self.project_name}, task: {self.task_name}, accomplished: {self.task_fulfilment}, deadline: {self.task_deadline}"


class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(length=30), default="Developer")
    salary = db.Column(db.Integer(), nullable=False, default=500)
    bonus = db.Column(db.Integer(), nullable=False, default=0)
    task_name = db.Column(db.String(length=30))
    project_name = db.Column(db.String(length=30))

    def __repr__(self):
        return f"Username: {self.username}, role: {self.role}"
