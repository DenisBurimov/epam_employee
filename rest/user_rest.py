from service import db
from models.models import User
from flask_login import current_user


class UserREST():
    def get(self):
        """
        Method checks if current user is admin or product owner.
        If yes, method returns all users.
        If role is PM method returns only users from PM's project
        """
        users = None
        if current_user.role == "admin" or current_user.role == "PO":
            users = User.query.all()
        elif current_user.role == "PM":
            users = User.query.filter_by(project_name=current_user.project_name)

        return users

    def get_user_details(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        # task = Task.query.filter_by(task_name=user.task_name).first()
        # user.task_id = task.task_id
        return user

    def post(self, username, email, hashed_password):
        """
        Method receives parameters of users.
        :param username:
        :param email:
        :param hashed_password:
        Then creates an instance of User class,
        passes all parameters and saves this instance to the db.
        """
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def put_by_user(self, username, email):
        """
        This method updates username and email by user.
        Method receives username and email from the view
        :param username:
        :param email:
        and then overwrites user with new parameters
        """
        current_user.username = username
        current_user.email = email
        db.session.commit()

    def put_by_admin(self,user_id, role, salary, bonus, task_name, project_name):
        """
        This method updates user parameters by admin or PM.
        Method receives parameters from view:
        :param user_id:
        :param role:
        :param salary:
        :param bonus:
        :param task_name:
        :param project_name:
        Then queries to the db and gets user by user_id
        and overwrites user with new parameters
        """
        user = User.query.filter_by(user_id=user_id).first()
        user.role = role
        user.salary = salary
        user.bonus = bonus
        user.task_name = task_name
        user.project_name = project_name
        db.session.commit()

