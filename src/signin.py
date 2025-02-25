from invalidcredentialserror import InvalidCredentialsError

class SignIn:
    def __init__(self, user_repo, hash_service):
        self.user_repo = user_repo
        self.hash_service = hash_service

    def perform(self, user_email, user_password):
        user = self.user_repo.find_by_email(user_email)
        if not user:
            raise InvalidCredentialsError()
        if self.hash_service.check(user_password, user.password):
            return True
        raise InvalidCredentialsError()