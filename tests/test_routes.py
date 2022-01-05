import unittest
from service import app


class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self) -> None:
        pass

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_login_page_loading(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        assert b"Log in" in response.data

    def test_login(self):

        tester = self.app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )

        self.assertIn(b"This app", response.data)

    def test_register_page_response(self):
        tester = app.test_client(self)
        response = tester.get("/register", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_register_page_loading(self):
        tester = app.test_client(self)
        response = tester.get("/register", content_type="html/text")
        assert b"Join Our Team" in response.data

    def test_register(self):

        tester = self.app.test_client(self)
        response = tester.post(
            '/register',
            data=dict(username="user96", email="mail96@company.com", password="123456", confirm_password="123456"),
            follow_redirects=True
        )

        self.assertIn(b"Registration", response.data)

    def test_project_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/projects", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_projects_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/projects", content_type="html/text")
        assert b"Current Projects" in response.data

    def test_tasks_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/tasks", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_tasks_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/tasks", content_type="html/text")
        assert b"Tasks" in response.data

    def test_users_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/users", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_users_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/users", content_type="html/text")
        assert b"Tasks" in response.data

    def test_add_project_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/add_project", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_add_project_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/add_project", content_type="html/text")
        assert b"Tasks" in response.data

    def test_task_adding_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/task_adding", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_task_adding_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/task_adding", content_type="html/text")
        assert b"Create New Task" in response.data

    def test_user_updating_by_admin_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/users/18", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_user_updating_by_admin_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/users/18", content_type="html/text")
        assert b"George Orwell" in response.data

    def test_user_updating_by_user_page(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/account", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_user_updating_by_user_page_loading(self):
        tester = app.test_client(self)
        logg = tester.post(
            '/login',
            data=dict(email="denysburimov@gmail.com", password="123456"),
            follow_redirects=True
        )
        response = tester.get("/account", content_type="html/text")
        assert b"Username" in response.data


if __name__ == '__main__':
    unittest.main()
