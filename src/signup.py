from user import User
from duplicateusererror import DuplicateUserError
from invalidpassworderror import InvalidPasswordError
from invalidpassworderror import InvalidPasswordError


class SignUp:

    def __init__(self, userrepo, hash_service):
        self.userrepo = userrepo
        self.hash_service = hash_service

    def perform(self, user_name, user_email, user_password):
        if invalid(user_password):
            raise InvalidPasswordError()
        if self.userrepo.find_by_email(user_email) != None:
            raise DuplicateUserError()
        hashed_pwd = self.hash_service.hash(user_password)
        user = User(user_name, user_email, hashed_pwd)
        self.userrepo.add(user)
        return True


def invalid(user_password):
    if not contain_lower_letter(user_password):
        raise InvalidPasswordError
    if not contain_upper_letter(user_password):
        raise InvalidPasswordError
    if not contain_number(user_password):
        raise InvalidPasswordError
    if not contain_special(user_password):
        raise InvalidPasswordError
    if not min_size(user_password):
        raise InvalidPasswordError
    if not max_size(user_password):
        raise InvalidPasswordError


def contain_lower_letter(user_password):
    for c in user_password:
        if c.islower():
            return True
    return False


def contain_upper_letter(user_password):
    for c in user_password:
        if c.isupper():
            return True
    return False


def contain_number(user_password):
    for c in user_password:
        if c.isdecimal():
            return True
    return False


def contain_special(user_password):
    for c in user_password:
        if not c.isalnum():
            return True
    return False


def min_size(user_password):
    return len(user_password) >= 6


def max_size(user_password):
    return len(user_password) <= 15