from ..models import User

class UserRepository:
    def __init__(self, model=None):
        self.model = User

    def create_user(self, **kwargs):
        user = self.model.objects.create(**kwargs)
        user.save()