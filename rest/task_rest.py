from service import db
from models.models import Project, Task, User
from flask_login import current_user
from datetime import date


class TaskREST():
    def get(self):
        """
        Method gets data from db and passes to the views.
        Get method checks if current user has a project.
        If he has, then queries from db only tasks from this project.
        If current user is admin or PO and has no project,
        then get method queries all tasks.
        Then creates an empty list, that fills with
        existing parameters of each task
        and additionally fills with calculated values as
        delta - difference between deadline and current date
        timedifference - dalta in days format

        Then, looping through our users, that are on this task
        and adds these users to each task objects.
        """
        if current_user.project_name:
            tasks_selected = Task.query.filter_by(project_name=current_user.project_name)
        else:
            tasks_selected = Task.query.all()

        tasks_to_pass = []
        for tasks_query in tasks_selected:
            delta = tasks_query.task_deadline - date.today()
            tasks_query.timedifference = delta.days
            tasks_query.users = User.query.filter_by(task_name=tasks_query.task_name)
            tasks_to_pass.append(tasks_query)

        return tasks_to_pass

    def get_task_details(self, task_id):
        """

        :param task_id:
        :return:
        """
        task = Task.query.filter_by(task_id=task_id).first()
        project = Project.query.filter_by(project_name=task.project_name).first()
        task.project_id = project.project_id
        return task

    def post(self, project_name, task_name, task_fulfilment, task_started, task_deadline):
        """
        Method receives task parameters and saves the task to the db.
        Receiving task parameters from the views.
        Creating an instance of the Task class
        and saving this instance to the db.
        :param project_name:
        :param task_name:
        :param task_fulfilment:
        :param task_started:
        :param task_deadline:
        :return:
        """
        task = Task(
            project_name=project_name,
            task_name=task_name,
            task_fulfilment=task_fulfilment,
            task_started=task_started,
            task_deadline=task_deadline
        )
        db.session.add(task)
        db.session.commit()

    def put(self, task_id, project_name, task_name, task_fulfilment, task_started, task_deadline):
        """
        Method receives parameters of the task, that we want to update.
        :param task_id:
        :param project_name:
        :param task_name:
        :param task_fulfilment:
        :param task_started:
        :param task_deadline:
        Makes a query to the db, gets the task by task_id.
        Overwrites the task data to the db.
        """
        task = Task.query.filter_by(task_id=task_id).first()
        task.project_name = project_name
        task.task_name = task_name
        task.task_fulfilment = task_fulfilment
        task.task_started = task_started
        task.task_deadline = task_deadline
        db.session.commit()

    def delete(self, task_id):
        """
        Method receives id of the task, that we have to delete,
        queries to db by this task_id and deletes this task
        """
        task = Task.query.filter_by(task_id=task_id).first()
        db.session.delete(task)
        db.session.commit()
