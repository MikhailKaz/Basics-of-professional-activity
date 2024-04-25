import unittest
from dataclasses import dataclass
from app import create_app
from app.models import User
from app.forms import LoginForm


@dataclass
class Login:
    login: str
    password: str


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()
        self.client.application.config["WTF_CSRF_ENABLED"] = False


    def test_login_success(self):
        with self.client.application.app_context():
            user = User.all()[0]

            form = LoginForm(formdata=None, obj=Login(user.login, user.password))
            res = self.client.post("/login", follow_redirects=True, data=form.data)
            assert res.status_code == 200, f"expected status code 200, received {res.status_code}"
            assert res.request.path == "/", f"expected redirect to '/', received '{res.request.path}'"


    def test_login_fail(self):
        with self.client.application.app_context():
            form = LoginForm(formdata=None, obj=Login("1 23", "a"))
            res = self.client.post("/login", data=form.data)
            assert res.status_code == 200, f"expected 200, received {res.status_code}"
            assert res.request.path == "/login", f"expected '/login', received '{res.request.path}'"


if __name__ == "__main__":
    unittest.main()
