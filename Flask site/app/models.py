# Flask modules
from flask_login import UserMixin

_users = []

class User(UserMixin):
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    @staticmethod
    def all():
        global _users
        if len(_users) > 0:
            return _users
        with open("users.txt") as f:
            for line in f:
                id, login, password = line.split()
                _users.append(User(id, login, password))
        return _users

    @staticmethod
    def find_by_id(id):
        found = list(filter(lambda x: x.id == id, User.all()))
        return None if len(found) == 0 else found[0]

    @staticmethod
    def find_by_creds(login, password):
        found = list(filter(lambda x: x.login == login and x.password == password, User.all()))
        return None if len(found) == 0 else found[0]
