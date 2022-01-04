from service import db
from models.models import Project, Task, User
from datetime import date

all_projects = Project.query.all()

# for item in all_projects:
#     print(type(item), item)

another_project = project = Project(
    project_name="Testing Project 1",
    fulfilment=0,
    project_started=date(2022, 1, 1),
    project_deadline=date(2023, 1, 1)
)
db.session.add(project)
db.session.commit()