from ..models import UserAdditionalData


class UserAdditionalDataRepository:
    def __init__(self):
        self.__user_additional_data_model = UserAdditionalData


    def add_new(self, user):
        new_object = self.__user_additional_data_model(user=user)
        new_object.save()
        return new_object
    
    
    def save_middle_name_for_user(self, user, new_middle_name):
        user_additional_data = self.__user_additional_data_model.objects.get(user=user)
        user_additional_data.middle_name = new_middle_name
        user_additional_data.save()
    

    def get_middle_name_for_user(self, user):
        user_additional_data = self.__user_additional_data_model.objects.get(user=user)
        return user_additional_data.middle_name
    

    def get_object_by_user(self, user):
        return self.__user_additional_data_model.objects.get(user=user)
    

    def get_object_by_code(self, code):
        return self.__user_additional_data_model.objects.get(code=code)
