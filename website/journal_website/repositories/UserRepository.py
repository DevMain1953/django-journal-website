from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject


class UserRepository:
    def __init__(self):
        self.__user_model = User
    

    def is_user_reviewer(self, user: SimpleLazyObject) -> bool:
        return user.groups.filter(name="Reviewers").exists()
