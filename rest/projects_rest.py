from service import db
from models.models import Project, Task, User
from flask_login import current_user
from datetime import date
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
filehandler = logging.FileHandler('projects_logger.log')
filehandler.setLevel(logging.INFO)
filehandler.setFormatter(log_formatter)
logger.addHandler(filehandler)


class ProjectREST():
    def get(self):
        """
        Method gets data from db and passes to the views.
        Get method checks if current user has a project.
        If he has, then queries from db only this project.
        If current user is admin or PO and has no project,
        then get method queries all projects.
        Then creates an empty list, that fills with
        existing parameters of each project
        and additionally fills with calculated values as
        delta - difference between deadline and current date
        timedifference - delta in days format

        Then, looping through our users, that are on this project,
        we calculate the total salary and bonuses on this project.
        After that we calculate what we have to pay till the end of the project
        and calculate what we already have spent on this project.

        All this data we append to the new list and return it
        """
        if current_user.project_name:
            projects_selected = Project.query.filter_by(project_name=current_user.project_name)
        else:
            projects_selected = Project.query.all()
        projects_info = []
        for project_query in projects_selected:
            delta = project_query.project_deadline - date.today()
            project_query.timedifference = delta.days

            project_query.users = User.query.filter_by(project_name=project_query.project_name)
            project_query.salary_plus_bonuses = 0
            for each_user in project_query.users:
                project_query.salary_plus_bonuses += each_user.salary + each_user.bonus

            # Now we make a total paid at the moment
            project_query.time_since_started = (date.today() - project_query.project_started).days
            project_query.currently_paid = project_query.time_since_started * project_query.salary_plus_bonuses // 30

            # Expected total payments, when the project will be done
            project_query.yet_to_pay = project_query.timedifference * project_query.salary_plus_bonuses // 30
            project_query.expected_total_payments = project_query.yet_to_pay + project_query.currently_paid

            projects_info.append(project_query)

        return projects_info

    def post(self, project_name, fulfilment, project_started, project_deadline):
        """
        Method receives project parameters and saves the project to the db.
        Receiving project parameters from the views.
        Creating an instance of the Project class
        and saving this instance to the db.
        :param project_name:
        :param fulfilment:
        :param project_started:
        :param project_deadline:
        """
        project = Project(
            project_name=project_name,
            fulfilment=fulfilment,
            project_started=project_started,
            project_deadline=project_deadline
        )
        db.session.add(project)
        db.session.commit()
        logger.info(f"Project {project_name} added by {current_user}: fulfilment {fulfilment}, project_started {project_started}, project_deadline {project_deadline}")


    def get_project_details(self, project_id):
        """
        Method receives from the views project_id - id of the project,
        witch details we want to see on the single project page
        Makes a query to the db and gets the project by project id.
        In addition to the db data (project_name, fulfilment, project_started, project_deadline)
        method calculates how many days is after the start,
        amount of salary and bonuses of the team,
        how much money is spent since the project is started,
        how many days team has till deadline,
        how much money is supposed to spend before the project ends,
        what tasks are on the project,
        who is on this project.

        returns a tuple with two elements:
        1) dict with certain project
        2) dict with tasks of this project and team members of this project
        returns a render of the html-page, that receives as parameters
        variable with project info and variable with tasks and users info
        """
        project = Project.query.get(project_id)
        delta = project.project_deadline - date.today()
        project.timedifference = delta.days

        project.users = User.query.filter_by(project_name=project.project_name)
        project.salary_plus_bonuses = 0
        for each_user in project.users:
            project.salary_plus_bonuses += each_user.salary + each_user.bonus

        # Now we make a total paid at the moment
        project.time_since_started = (date.today() - project.project_started).days
        project.currently_paid = project.time_since_started * project.salary_plus_bonuses // 30

        # Expected total payments, when the project will be done
        project.yet_to_pay = project.timedifference * project.salary_plus_bonuses // 30
        project.expected_total_payments = project.yet_to_pay + project.currently_paid

        tasks = []
        for tasks_query in Task.query.filter_by(project_name=project.project_name):
            delta = tasks_query.task_deadline - date.today()
            tasks_query.timedifference = delta.days
            tasks_query.users = User.query.filter_by(task_name=tasks_query.task_name)
            tasks.append(tasks_query)

        return (project, tasks)

    def put(self, project_id, project_name, fulfilment, project_started, project_deadline):
        """
        Method receives parameters of the project, that we want to update.
        Makes a query to the db, gets the project by project_id.
        Overwrites the project data to the db.
        """
        project = Project.query.filter_by(project_id=project_id).first()
        project.project_name = project_name
        project.fulfilment = fulfilment
        project.project_started = project_started
        project.project_deadline = project_deadline
        db.session.commit()
        logger.info(f"Project {project_name} updated by {current_user}: fulfilment {fulfilment}, project_started {project_started}, project_deadline {project_deadline}")


    def delete(self, project_id):
        """
        Method receives id of the project, that we have to delete,
        queries to db by this project_id and deletes this project
        """
        project = Project.query.get_or_404(project_id)
        logger.info(f"Project {project.project_name} deleted by {current_user}")
        db.session.delete(project)
        db.session.commit()
