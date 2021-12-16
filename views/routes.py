from service import app, db, bcrypt
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
    projects = Project.query.all()
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('home.html', projects=projects, tasks=tasks, users=users)


@app.route("/projects")
def projects():
    """
    Здесь вьюшка импортирует класс из реста,
    создаёт экземпляр этого класса,
    и этот экземпляр выполняет метод гет,
    который возвращает список проектов.
    *Правда, надо сделать json
    функция возвращает рендер html-страницы projects.html,
    в который она передайт список проектов (projects=projects_info)
    """
    projects_query = ProjectREST()
    projects_info = projects_query.get()

    return render_template('projects.html', projects=projects_info)


@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    """
    Здесь создаём экземпляр класса формы создания проекта
    Затем, если форма проходит валидацию,
    то создаём экземпляр класса ProjectREST
    и вызываем его метод пост
    После чего возвращаем ридайрект на страницу списка проектов
    :return: рендерим страницу добавления проекта, если не было отправки формы либо не было валидации
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
    Эта функция для отображения всех деталей проекта
    включая задания на проекте и команду проекта
    Получаем ид проекта из адресной строки
    :param project_id:
    Создаём экземпляр класса ProjectREST
    Его метод get_details возвращает нам тюпл из двух элементов:
    первый элемент - словарь проекта
    второй элемент - словарь заданий и участников команды
    :return: рендер html-страницы, в который мы передаём проект и задания
    """
    project_query = ProjectREST()
    get_getails = project_query.get_project_details(project_id)
    project = get_getails[0]
    tasks = get_getails[1]

    return render_template('project_details.html', project=project, tasks=tasks)


@app.route("/projects/update/<int:project_id>", methods=['GET', 'POST'])
def project_update(project_id):
    """
    Создаём форму - экземпляр класса ProjectUpdate
    Создаём экземпляр класса ProjectREST,
    чтобы с помощью его метода put внести изменения,
    и чтобы с помощью его метода get_details отобразить данные о проекте в форме
    :param project_id: передаём в метод  get_details

    Если форма проходит валидацию и имя проекта не занято,
        передаём в метод put класса ProjectREST параметры:
        project_id, project_name, fulfilment, project_started, project_deadline
        возвращаем редайрект на страницу с проектами
        :return: redirect(url_for('projects'))
или передаём, что имя занято

    Если используется не метод PUT, а метод GET,  то выводим в поля формы текущие данные о проекте
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
    создаём экземпляр класса ProjectREST
    и передаём в его метод delete параметр project_id
    :param project_id:
    метод delete удаляет проект,
    после чего мы вызываем сообщение об успехе
    и возвращаем редайрект на страницу проектов
    :return:
    """
    project_query = ProjectREST()
    project_deleted = project_query.delete(project_id)
    flash("The project was successfully deleted", "success")
    return redirect(url_for('projects'))


@app.route("/tasks")
def tasks():
    """
    Создаём экземпляр класса TaskREST
    с тем, чтобы его метод get вернул список заданий
    Возвращаем рендер страницы, в который передаём список заданий и текущего пользователя
    :return:
    """
    task_query = TaskREST()
    tasks_to_pass = task_query.get()

    return render_template('tasks.html', tasks=tasks_to_pass, c_user=current_user)


@app.route("/task_adding", methods=['GET', 'POST'])
def task_adding():
    """
    Создаём форму на основе класса TaskCreate
    Создаём экземпляр класса TaskREST,
    чтобы его метод post записал в базу новое задание
    В метод post передаём параметры.
    Выводим флеш сообщение, что всё хорошо
    Возвращаем редайрект на страницу с заданиями
    :return:
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
    Создаём форму на основе класса TaskUpdate
    создаём экземпляр класса TaskREST,
    чтобы его метод get_task_details вернул нам данные о задании,
    а его метод put апдейтнул задание
    В методы get_task_details и put мы передаём task_id
    :param task_id:
    Дальше, если форма валидирована и имя имя задания уникально,
    вызываем метод put и передаём в него все параметры задания
    В случае успеха выводится флеш сообщение об успехе
    и возвращается ридайрект на страницу проекта
    Если имя занято, выводится сообщение об этом
    Если форма пуста, то в неё передаются данные из метода get_task_details
    и возвращается рендер страницы, в который передаются пропертиз задания
    :return:
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
    Создаём форму на основе класса TaskUpdate
    создаём экземпляр класса TaskREST,
    чтобы его метод get_task_details вернул нам данные о задании,
    а его метод delete удалил задание
    В методы get_task_details и delete мы передаём task_id
    :param task_id:
    :return:
    """
    task_query = TaskREST()
    task = task_query.get_task_details(task_id)
    task_deleted = task_query.delete(task_id)

    flash(f"{task.task_name} was successfully deleted", "success")

    return redirect(url_for('project_details', project_id=task.project_id))


@app.route("/users")
def users():
    """

    :return:
    """
    users_query = UserREST()
    users = users_query.get()

    return render_template('users.html', users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """

    :return:
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
    """

    :return:
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

    :param user_id:
    :return:
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
