from inmemoryuserrepository import InMemoryUserRepository
from signup import SignUp
from signin import SignIn
import pytest
from duplicateusererror import DuplicateUserError
from invalidpassworderror import InvalidPasswordError
from invalidcredentialserror import InvalidCredentialsError
from fakehashservice import FakeHashService


def test_signup_with_valid_data():
    hash_service = FakeHashService()
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234TEST&'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    assert user_repo.find_by_email(user_email).name == user_name


def test_prevent_duplicate_user():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234TEST&'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    dup_user_name = 'Doe Joe'
    dup_user_email = 'joe@doe.com'
    dup_user_password = 'TEST1234test&'
    with pytest.raises(DuplicateUserError):
        usecase.perform(dup_user_name, dup_user_email, dup_user_password)


def test_hash_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234TEST&'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    saved_user = user_repo.find_by_email(user_email)
    assert saved_user.name == user_name
    assert saved_user.password != user_password
    assert hash_service.check(user_password, saved_user.password)


def test_password_lower_case_letter():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'TEST1234TEST&'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_password_upper_case_letter():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234test&'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_password_number():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'testTESTtest&'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_password_special_character():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'TEST1234testE'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_password_too_short():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'tE1&C'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_password_too_long():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'tE1&CtE1&CtE1&Ct'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_valid_signin():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234TEST&'
    signup = SignUp(user_repo, hash_service)
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    assert usecase.perform(user_email, user_password) == True


def test_signin_wrong_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test1234TEST&'
    signup = SignUp(user_repo, hash_service)
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform(user_email, 'WRONG_PASSWORD')


def test_signin_invalid_user():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform('invalid@user.com', '234TEST&')


def test_password_lowercase_letter():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = '1234TEST&'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)


def test_successful_signin():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = '1234TeST&'
    signup = SignUp(user_repo, hash_service)
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    assert usecase.perform(user_email, user_password) == True


def test_signin_wrong_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = '1234TeST&'
    signup = SignUp(user_repo, hash_service)
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform(user_email, 'WRONG_PASSWORD')


def test_signin_invalid_user():
    user_repo = InMemoryUserRepository
    hash_service = FakeHashService
    signup = SignUp(user_repo, hash_service)
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = '1234TeST&'
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform('WRONG_EMAIL', user_password)
