from django.contrib.auth.models import User


class UserRepository:
    def __init__(self):
        self.__user_model = User
    

    def is_user_member_of_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()
