from service import db
from models.models import Project, Task, User
from flask_login import current_user
from datetime import date


class TaskREST():
    def get(self):
        """
        Метод гет сначала проверяет, есть ли у текущего юзера назначенный проект.
        Если есть, то запрос в базу состоит только из заданий назначенного проекта.
        Если назначенного проекта нет (например нет у владельца или администратора),
        то возвращается список всех заданий.
        Дальше создаём пустой список, который потом будем возвращать
        и запускаем цикл по запросу из базы
        В каждой итерации вычисляем следующие параметры:
        delta - разница между текущей датой и дедлайном задания
        timedifference - это дельта, переведённая в формат только дней

        Из модели класса юзер запрашиваем всех юзеров на этом задании
        Формируем список заданий с данными полями
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
        task = Task.query.filter_by(task_id=task_id).first()
        project = Project.query.filter_by(project_name=task.project_name).first()
        task.project_id = project.project_id
        return task

    def post(self, project_name, task_name, task_fulfilment, task_started, task_deadline):
        """
        Принимаем параметры для создания экземпляра класса Project
        :param project_name:
        :param fulfilment:
        :param project_started:
        :param project_deadline:
        Сохраняем проект в базу
        :return: None
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
        Если форма апдейта проекта валидирована,
        получаем из вьюшки параметры записи в базу:
        :param project_id:
        :param project_name:
        :param fulfilment:
        :param project_started:
        :param project_deadline:
        Делаем запрос в базу экземпляра класс экземпляра Project с заданным ид
        и перезаписываем поля этого класса, используя полученные из вьюшки параметры
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
        Получаем из вьюшки ид задания
        Делаем запрос в базу и получаем задание с данным ид
        Удаляем задание из базы
        Коммитим изменения в базе
        :return:
        """
        task = Task.query.filter_by(task_id=task_id).first()
        db.session.delete(task)
        db.session.commit()
