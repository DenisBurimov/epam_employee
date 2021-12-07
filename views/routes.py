from service import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from models.models import Project, Task, User
from datetime import date
from service.forms import RegistrationForm, LoginForm, UpdateAccount, UsersManagement, ProjectUpdate, ProjectCreate, TaskCreate
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
    """

    :return:
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

    return render_template('projects.html', projects=projects_info)


@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    form = ProjectCreate()
    if form.validate_on_submit():
        project = Project(project_name=form.project_name.data, fulfilment=form.fulfilment.data, project_started=form.project_started.data, project_deadline=form.project_deadline.data)
        db.session.add(project)
        db.session.commit()
        flash(f"Project has been successfully created", "success")
        return redirect(url_for('projects'))
    return render_template('add_project.html', title='Add Project', form=form)


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


@app.route("/projects/update/<int:project_id>", methods=['GET', 'POST'])
def project_update(project_id):
    form = ProjectUpdate()
    project = Project.query.filter_by(project_id=project_id).first()
    if form.validate_on_submit():
        project.project_name = form.project_name.data
        project.fulfilment = form.fulfilment.data
        project.project_started = form.project_started.data
        project.project_deadline = form.project_deadline.data
        db.session.commit()
        flash(f"{project} has been updated", "success")
        return redirect(url_for('projects'))
    elif request.method == 'GET':
        form.project_name.data = project.project_name
        form.fulfilment.data = project.fulfilment
        form.project_started.data = project.project_started
        form.project_deadline.data = project.project_deadline

    return render_template('project_update.html', title="Project Update", project=project, form=form)

@app.route("/projects/delete/<int:project_id>", methods=['GET', 'POST'])
def project_deleting(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("The project was successfully deleted", "success")

    return redirect(url_for('projects'))

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


@app.route("/task_adding", methods=['GET', 'POST'])
def task_adding():
    form = TaskCreate()
    if form.validate_on_submit():
        task = Task(
            project_name=form.project_name.data,
            task_name=form.task_name.data,
            task_fulfilment=form.task_fulfilment.data,
            task_started=form.task_started.data,
            task_deadline=form.task_deadline.data
        )
        db.session.add(task)
        db.session.commit()
        flash(f"Task {form.task_name.data} has been successfully created", "success")
        return redirect(url_for('tasks'))
    return render_template('task_adding.html', title='Add Task', form=form)


@app.route("/task_update/<int:task_id>", methods=['GET', 'POST'])
def task_update(task_id):
    form = TaskCreate()
    task = Task.query.filter_by(task_id=task_id).first()
    project = Project.query.filter_by(project_name=task.project_name).first()
    if form.validate_on_submit():
        task.project_name = form.project_name.data
        task.task_name = form.task_name.data
        task.task_fulfilment = form.task_fulfilment.data
        task.task_started = form.task_started.data
        task.task_deadline = form.task_deadline.data
        db.session.commit()
        flash(f"{task} has been updated", "success")
        return redirect(url_for('project_details', project_id=project.project_id))
    elif request.method == 'GET':
        form.project_name.data = task.project_name
        form.task_name.data = task.task_name
        form.task_fulfilment.data = task.task_fulfilment
        form.task_started.data = task.task_started
        form.task_deadline.data = task.task_deadline

    return render_template('task_update.html', title='Update Task', form=form, task=task)


@app.route("/task_delete")
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.filter_by(project_name=task.project_name).first()
    db.session.delete(task)
    db.session.commit()
    flash(f"{task.task_name} was successfully deleted", "success")

    return redirect(url_for('project_details', project_id=project.project_id))


@app.route("/users")
def users():
    users = None
    if current_user.role == "admin" or current_user.role == "PO":
        users = User.query.all()
    elif current_user.role == "PM":
        users = User.query.filter_by(project_name=current_user.project_name)

    return render_template('users.html', users=users)


@app.route("/users/<int:user_id>", methods=['GET', 'POST'])
def user_details(user_id):
    form = UsersManagement()
    user = User.query.filter_by(user_id=user_id).first()
    if form.validate_on_submit():
        user.role = form.role.data
        user.salary = form.salary.data
        user.bonus = form.bonus.data
        user.task_name = form.task_name.data
        user.project_name = form.project_name.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('users'))
    elif request.method == 'GET':
        form.role.data = user.role
        form.salary.data = user.salary
        form.bonus.data = user.bonus
        form.task_name.data = user.task_name
        form.project_name.data = user.project_name
    return render_template('user_details.html', title='User Details', user=user, form=form)


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)
