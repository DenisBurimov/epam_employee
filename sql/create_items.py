from service import db
from models.models import Project, Task, User
from datetime import date

pr1 = Project(project_name="First Project", project_started=date(2021, 1, 1), project_deadline=date(2022, 1, 1))
t1 = Task(project_name="First Project", task_name="First Task", task_started=date(2021, 1, 1), task_deadline=date(2022, 1, 1))
u1 = User(username="User1", email="mail1@company.com", hashed_password="123456")

db.session.add(pr1)
db.session.commit()