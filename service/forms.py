from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.models import User, Task, Project
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UsersManagement(FlaskForm):
    role = StringField('Role', validators=[DataRequired(), Length(min=2, max=20)])
    salary = IntegerField('Salary')
    bonus = IntegerField('Bonus')
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=2, max=20)])
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')


class ProjectUpdate(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    fulfilment = IntegerField('Accomplished')
    project_started = DateField('Project started')
    project_deadline = DateField('Project Deadline')
    submit = SubmitField('Update')


class ProjectCreate(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    fulfilment = IntegerField('Accomplished')
    project_started = DateField('Project started')
    project_deadline = DateField('Project Deadline')
    submit = SubmitField('Create Project')

    def validate_project_name(self, project_name):
        project = Project.query.filter_by(project_name=project_name.data).first()
        if project:
            raise ValidationError('That project name is already taken. Please choose a different one.')


class TaskCreate(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=2, max=20)])
    task_fulfilment = IntegerField('Accomplished')
    task_started = DateField('Task started')
    task_deadline = DateField('Task Deadline')
    submit = SubmitField('Submit')

    def validate_task_name(self, task_name):
        task = Task.query.filter_by(task_name=task_name.data).first()
        if task:
            raise ValidationError('That task name is already taken. Please choose a different one.')


class TaskUpdate(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=20)])
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=2, max=20)])
    task_fulfilment = IntegerField('Accomplished')
    task_started = DateField('Task started')
    task_deadline = DateField('Task Deadline')
    submit = SubmitField('Submit')