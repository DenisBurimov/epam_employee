import unittest
from service import app, db
from models.models import Project
from datetime import date


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self) -> None:
        pass

    def test_project_adding(self):
        tester = app.test_client(self)

        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )

        adding = tester.post(
            '/add_project',
            data=dict(
                project_name="Testing Project",
                fulfilment=10,
                project_started=date(2022, 1, 1),
                project_deadline=date(2023, 1, 1),
            ),
            follow_redirects=True
        )
        response = tester.get("/projects", content_type="html/text")
        assert b"Testing Project" in response.data

    # def test_project_updating(self):
    #     tester = app.test_client(self)
    #
    #     logg = tester.post(
    #         '/login',
    #         data=dict(email="denysburimov@gmail.com", password="123456"),
    #         follow_redirects=True
    #     )
    #
    #     project = Project.query.filter_by(project_name="Testing Project").first()
    #
    #     adding = tester.put(
    #         f'/projects/update/{project.project_id}',
    #         data=dict(
    #             project_name="Testing Project 2",
    #             fulfilment=20,
    #         ),
    #         follow_redirects=True,
    #         content_type="html/text"
    #     )
    #     response = tester.get("/projects", content_type="html/text")
    #     assert b"Testing Project" in adding.data

    def test_project_deleting(self):
        tester = app.test_client(self)

        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )

        project = Project.query.filter_by(project_name="Testing Project").first()

        db.session.delete(project)
        db.session.commit()

        response = tester.get("/projects", content_type="html/text")
        assert b"Testing Project" not in response.data

