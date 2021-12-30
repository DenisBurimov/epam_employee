import unittest
from service import app


class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

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

    # def test_registration(self):
    #
    #     tester = self.app.test_client(self)
    #     response = tester.post(
    #         '/register',
    #         data=dict(username="user96", email="mail96@company.com", password="123456", confirm_password="123456"),
    #         follow_redirects=True
    #     )
    #
    #     self.assertIn(b"This app", response.data)


if __name__ == '__main__':
    unittest.main()
