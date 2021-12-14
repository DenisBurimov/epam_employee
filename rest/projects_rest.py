from service import app, db
from flask import Flask, render_template, jsonify, request, redirect
from models.models import Project, Task, User
from flask_login import current_user
from datetime import date
from flask_restful import Resource, Api

# api = Api(app)


class PostREST():
    def get(self):
        """
        Метод гет сначала проверяет, есть ли у текущего юзера назначенный проект.
        Если есть, то запрос в базу состоит только из назначенного проекта.
        Если назначенного проекта нет (например нет у владельца или администратора),
        то возвращается список всех проектов.
        Дальше создаём пустой список, который потом будем возвращать
        и запускаем цикл по запросу из базы
        В каждой итерации вычисляем следующие параметры:
        delta - разница между текущей датой и дедлайном
        timedifference - это дельта, переведённая в формат только дней

        В цикле, который проходит по всем юзерам, у которых назначен этот проект,
        вычисляем размер зарплаты и бонуса
        Затем перемножаем эту цифру и количество дней, которые длится проект,
        и получаем сколько уже заплачено

        Затем умножаем сумму зарплат и бонусов команды на оставшиеся дни до дедлайна
        и узнаём предположительные затраты до завершения проекта.

        Затем запихиваем данный словарь в projects_info
        :return: projects_info - список проектов (надо сделать json)
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

        return projects_info

    def post(self, project_name, fulfilment, project_started, project_deadline):
        """
        Принимаем параметры для создания экземпляра класса Project
        :param project_name:
        :param fulfilment:
        :param project_started:
        :param project_deadline:
        Сохраняем проект в базу
        :return: None
        """
        project = Project(
            project_name=project_name,
            fulfilment=fulfilment,
            project_started=project_started,
            project_deadline=project_deadline
        )
        db.session.add(project)
        db.session.commit()

    def get_details(self, project_id):
        """
        Получаем ид проекта из вьюшки (там вызывается этот метод)
        :param project_id:
        С помощью ид делаем запрос конкретного проекта
        Вычисляем время проекта в работе и время до дедлайна
        Вычисляем суммарную зарплату и бонусы тех, кто на данном проекте
        Вычисляем затраченные средства со дня старта проекта
        Вычисляем ожидаемые затраты на зарплаты и бонусы до дедлайна

        Делаем запрос в базу по заданиям на этом конкретном проекте
        вычисляем временные показатели для каждого задания (в работе и до дедлайна)
        Делаем запрос в базу по участникам команды на каждом задании
        :return: (project, tasks)
        """
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

        return (project, tasks)

    def put(self):
        pass


    def delete(self):
        pass

# api.add_resource(PostREST, "/testing")