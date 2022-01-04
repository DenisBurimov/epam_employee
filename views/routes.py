from service import app, bcrypt
from flask import render_template, redirect, url_for, request, flash
from models.models import Project, Task, User
from service.forms import RegistrationForm, LoginForm, UpdateAccount, UsersManagement, ProjectUpdate, ProjectCreate, \
    TaskCreate, TaskUpdate
from flask_login import login_user, current_user, logout_user, login_required
from rest.projects_rest import ProjectREST
from rest.task_rest import TaskREST
from rest.user_rest import UserREST


@app.route("/")
@app.route("/home")
def home():
    """
    Home Page just returns the project documentation
    :return:
    """
    projects = Project.query.all()
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('home.html', projects=projects, tasks=tasks, users=users)


@app.route("/projects")
def projects():
    """
    This view creates instance of the ProjectREST class
    to execute the get method of this class.
    Get method returns a list of all projects
    """
    projects_query = ProjectREST()
    projects_info = projects_query.get()

    return render_template('projects.html', projects=projects_info)


@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    """
    This view creates a form as an instance of the ProjectCreate class
    Then if the form is validated on submit,
    we create an instance of the ProjectREST class
    to execute the post method of this class.
    Post method creates a project in the PEST API
    After that we raise a success message and redirect to the projects page
    """
    form = ProjectCreate()
    if form.validate_on_submit():
        project_query = ProjectREST()
        project_posted = project_query.post(
            project_name=form.project_name.data,
            fulfilment=form.fulfilment.data,
            project_started=form.project_started.data,
            project_deadline=form.project_deadline.data
        )
        flash(f"Project has been successfully created", "success")
        return redirect(url_for('projects'))
    return render_template('add_project.html', title='Add Project', form=form)


@app.route("/projects/<int:project_id>")
def project_details(project_id):
    """
    This is a function for displaying details of the given project.
    Receives the id of the project, creates ProjectREST class instance,
    and its method get_details returns a tuple with two elements:
    1) dict with certain project
    2) dict with tasks of this project and team members of this project
    returns a render of the html-page, that receives as parameters
    variable with project info and variable with tasks and users info
    """
    project_query = ProjectREST()
    get_getails = project_query.get_project_details(project_id)
    project = get_getails[0]
    tasks = get_getails[1]

    return render_template('project_details.html', project=project, tasks=tasks)


@app.route("/projects/update/<int:project_id>", methods=['GET', 'POST'])
def project_update(project_id):
    """
    Receives the id of the project, that we want to update.
    Creates a form as an instance of the ProjectUpdate class,
    creates an instance of the ProjectREST  class,
    calls  get_project_details method to get all the parameters of the given project
    and if the form is validated on submit
    starts try - except process to pass the new parameters
    with the put method to the REST API
    If project name isn't unique, raises a message about that
    If nothing posts, then just renders a form,
    filled with info from get_project_details method
    """
    form = ProjectUpdate()
    project_query = ProjectREST()
    project = project_query.get_project_details(project_id)
    if form.validate_on_submit() and (
            not form.project_name.data in Project.query.all() or form.project_name.data == project[0].project_name):
        try:
            project_updated = project_query.put(
                project_id=project_id,
                project_name=form.project_name.data,
                fulfilment=form.fulfilment.data,
                project_started=form.project_started.data,
                project_deadline=form.project_deadline.data
            )
            flash(f"{form.project_name.data} has been updated", "success")
            return redirect(url_for('projects'))
        except BaseException as e:
            flash(f"Project name is already taken", "danger")
            return redirect(url_for('projects'))
    elif request.method == 'GET':
        form.project_name.data = project[0].project_name
        form.fulfilment.data = project[0].fulfilment
        form.project_started.data = project[0].project_started
        form.project_deadline.data = project[0].project_deadline

    return render_template('project_update.html', title="Project Update", project=project[0], form=form)


@app.route("/projects/delete/<int:project_id>", methods=['GET', 'POST'])
def project_deleting(project_id):
    """
    Receives project_id of the project, that we want to delete,
    creates an instance of the ProjectREST class,
    calls delete method,
    flashes the success message
    and redirects to the projects page
    """
    project_query = ProjectREST()
    project_deleted = project_query.delete(project_id)
    flash("The project was successfully deleted", "success")
    return redirect(url_for('projects'))


@app.route("/tasks")
def tasks():
    """
    Creates an instance of the TaskREST class,
    calls get method, that returns the list of all tasks.
    Passes that list to the template
    """
    task_query = TaskREST()
    tasks_to_pass = task_query.get()

    return render_template('tasks.html', tasks=tasks_to_pass, c_user=current_user)


@app.route("/task_adding", methods=['GET', 'POST'])
def task_adding():
    """
    Creates form as an instance of the TaskCreate class.
    If the form is validated on submit,
    creates an instance of the TaskREST class,
    calls the post method and passes to it the parameters of the task:
    project_name, task_name, task_fulfilment, task_started, task_deadline
    Outputs a success message.
    Returns redirect to the tasks page
    """
    form = TaskCreate()
    if form.validate_on_submit():
        task_query = TaskREST()
        task_query.post(
            project_name=form.project_name.data,
            task_name=form.task_name.data,
            task_fulfilment=form.task_fulfilment.data,
            task_started=form.task_started.data,
            task_deadline=form.task_deadline.data
        )
        flash(f"Task {form.task_name.data} has been successfully created", "success")
        return redirect(url_for('tasks'))
    return render_template('task_adding.html', title='Add Task', form=form)


@app.route("/task_update/<int:task_id>", methods=['GET', 'POST'])
def task_update(task_id):
    """
    Receives the id of the task, that we want to update
    Creates a form as an instance of the TaskUpdate class.
    Creates an instance of the TaskREST class,
    calls get_task_details method and passes to it the task_id.
    Then if the form is validated on submit,
    check if task name is unique
    and launches the try - except construction to pass to the REST API
    all parameters of the task with put method.

    If nothing updates, just renders the form, filled with data
    from the get_task_details method
    """
    form = TaskUpdate()
    task_query = TaskREST()
    task = task_query.get_task_details(task_id)
    if form.validate_on_submit() and (
            not form.task_name.data in Task.query.all() or form.task_name.data == task.task_name):
        try:
            task_updated = task_query.put(
                task_id=task_id,
                project_name=form.project_name.data,
                task_name=form.task_name.data,
                task_fulfilment=form.task_fulfilment.data,
                task_started=form.task_started.data,
                task_deadline=form.task_deadline.data,
            )
            flash(f"{form.task_name.data} has been updated", "success")
            return redirect(url_for('project_details', project_id=task.project_id))
        except BaseException as e:
            flash(f"Task name is already taken", "danger")
            return redirect(url_for('project_details', project_id=task.project_id))
    elif request.method == 'GET':
        form.project_name.data = task.project_name
        form.task_name.data = task.task_name
        form.task_fulfilment.data = task.task_fulfilment
        form.task_started.data = task.task_started
        form.task_deadline.data = task.task_deadline

    return render_template('task_update.html', title='Update Task', form=form, task=task)


@app.route("/task_update/delete/<int:task_id>")
def task_delete(task_id):
    """
    Receives task_id of the task, that we want to delete,
    creates an instance of the TaskREST class,
    calls delete method,
    flashes the success message
    and redirects to the project_details page
    """
    task_query = TaskREST()
    task = task_query.get_task_details(task_id)
    task_deleted = task_query.delete(task_id)

    flash(f"{task.task_name} was successfully deleted", "success")

    return redirect(url_for('project_details', project_id=task.project_id))


@app.route("/users")
def users():
    """
    Creating instance of UserRest class,
    to use its get method
    This method returns from REST API the list of all users
    :return:
    Then we pass into the template users variable
    """
    users_query = UserREST()
    users = users_query.get()

    return render_template('users.html', users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    A classic registration method
    Firstly we create a form as a RegistrationForm class instance
    If form is validate on submit,
    username, email and hashed password are passed to REST API
    as arguments of the post method UserREST class
    If this post operation successful,
    we output flash message about success
    and return redirection to the home page
    :return:
    If not, returns render of the registration page template,
    that recieves as parameters title and form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_query = UserREST()
        user = user_query.post(
            username=form.username.data,
            email=form.email.data,
            hashed_password=hashed_password
        )
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Creating LoginForm instance
    Then, if this form is validated on submit,
    we check if user with given parameters exists in database
    and given password is equal to password in database,
    we log in user
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You are successfully logged in as a(n) {current_user.role}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """
    Standard built-in logout_user method of the flask_login module
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    This is form to change username and email by a user himself
    Other parameters are able to change by project manager of admin
    Creating a form as a RegistrationForm class instance
    If form is validate on submit,
    username, email are passed to REST API
    as arguments of the put method UserREST class
    If this post operation successful,
    we output flash message about success
    and return redirection to the account page
    :return:
    If not, returns render of the account page template,
    that recieves as parameters title and form
    and contains in form fields current user username and email
    """
    form = UpdateAccount()
    if form.validate_on_submit():
        user_query = UserREST()
        user = user_query.put_by_user(username=form.username.data, email=form.email.data)
        flash("Your account has been updated", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/users/<int:user_id>", methods=['GET', 'POST'])
def user_details(user_id):
    """
    This form is to change user's role, salary and bonus by PM or admin
    Receives the user_id
    :param user_id:
    Creating a form as a RegistrationForm class instance
    If form is validate on submit,
    role, salary and bonus are passed to REST API
    as arguments of the put method UserREST class
    If this post operation successful,
    we output flash message about success
    and return redirection to the account page
    :return:
    If not, returns render of the account page template,
    that receives as parameters title and form
    and contains in form fields role, salary and bonus of the user with given user_id
    """
    form = UsersManagement()
    user_query = UserREST()
    user = user_query.get_user_details(user_id)
    if form.validate_on_submit():
        user_updated = user_query.put_by_admin(
            user_id=user_id,
            role=form.role.data,
            salary=form.salary.data,
            bonus=form.bonus.data,
            task_name=form.task_name.data,
            project_name=form.project_name.data
        )
        flash("Your account has been updated", "success")
        return redirect(url_for('users'))
    elif request.method == 'GET':
        form.role.data = user.role
        form.salary.data = user.salary
        form.bonus.data = user.bonus
        form.task_name.data = user.task_name
        form.project_name.data = user.project_name
    return render_template('user_details.html', title='User Details', user=user, form=form)
