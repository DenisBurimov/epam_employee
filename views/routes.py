from service import app, db
from flask import render_template, redirect, url_for,request
from models.models import Project, Task, User

@app.route("/")
@app.route("/home")
def home():
    projects = Project.query.all()
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('home.html', projects=projects, tasks=tasks, users=users)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password1']
        new_user = User(username=username, email=email, role=role, hashed_password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html')
