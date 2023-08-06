from django.utils.functional import SimpleLazyObject


class UserRepository:
    def __init__(self):
        pass
    
    def is_user_reviewer(self, user: SimpleLazyObject) -> bool:
        return user.groups.filter(name="Reviewers").exists()
