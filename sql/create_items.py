from service import db
from models.models import Project, Task, User
from datetime import date

pr1 = Project(project_name="First Project", fulfilment=0, project_started=date(2021, 1, 1), project_deadline=date(2022, 1, 1))
t1 = Task(project_name="First Project", task_name="First Task", task_fulfilment=0, task_started=date(2021, 1, 1), task_deadline=date(2022, 1, 1))