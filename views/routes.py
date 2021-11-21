from service import app, db
from flask import render_template, redirect, url_for,request
from models.models import Project, Task, User
from datetime import date

@app.route("/")
@app.route("/home")
def home():
    projects = Project.query.all()
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('home.html', projects=projects, tasks=tasks, users=users)


@app.route("/tasks")
def tasks():
    objects = []
    for tasks_query in Task.query.all():
        delta = tasks_query.task_deadline - date.today()
        tasks_query.timedifference = delta.days
        objects.append(tasks_query)

    return render_template('tasks.html', passed_value=objects)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password1']
        new_user = User(username=username, email=email, hashed_password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html')
