from service import app, db
from flask import render_template, redirect, url_for,request, flash
from models.models import Project, Task, User
from datetime import date
from service.forms import RegistrationForm, LoginForm

@app.route("/")
@app.route("/home")
def home():
    projects = Project.query.all()
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('home.html', projects=projects, tasks=tasks, users=users)

@app.route("/projects")
def projects():
    # Only project names, fulfilment, dates, backlog, finances
    projects_info = []
    for project_query in Project.query.all():
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
        project_query.yet_to_pay = project_query.timedifference * project_query.salary_plus_bonuses //30
        project_query.expected_total_payments = project_query.yet_to_pay + project_query.currently_paid

        projects_info.append(project_query)

    return render_template('projects.html', projects=projects_info)


@app.route("/projects/<int:project_id>")
def project_details(project_id):
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

    return render_template('project_details.html', project=project, tasks=tasks)


@app.route("/tasks")
def tasks():
    tasks_to_pass = []
    for tasks_query in Task.query.all():
        delta = tasks_query.task_deadline - date.today()
        tasks_query.timedifference = delta.days
        tasks_query.users = User.query.filter_by(task_name=tasks_query.task_name)
        tasks_to_pass.append(tasks_query)

    return render_template('tasks.html', tasks=tasks_to_pass)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'mail1@company.com' and form.password.data == '123456':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)