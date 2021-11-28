from service import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from models.models import Project, Task, User
from datetime import date
from service.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


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
        project_query.yet_to_pay = project_query.timedifference * project_query.salary_plus_bonuses // 30
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

    return render_template('tasks.html', tasks=tasks_to_pass, c_user=current_user)

@app.route("/users")
def users():
    if current_user.role == "admin" or current_user.role == "PO":
        users = User.query.all()

    return render_template('users.html', users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
