import bcrypt
from hashservice import HashService


class BCryptHashService(HashService):

    def __init__(self, salt):
        self.salt = salt

    def hash(self, pwd):
        return bcrypt.hashpw(pwd.encode('utf-8'), self.salt)

    def check(self, pwd, hashed):
        return bcrypt.checkpw(pwd.encode('utf-8'), hashed)
