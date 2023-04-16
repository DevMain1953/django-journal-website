from django.contrib.auth.models import User


class UserRepository:
    def __init__(self):
        self.__user_model = User
    

    def is_user_reviewer(self, user):
        return user.groups.filter(name="Reviewers").exists()
