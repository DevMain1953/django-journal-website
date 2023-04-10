class UserAdditionalDataRepository:
    def __init__(self, model):
        self.user_additional_data_model = model


    def save_middle_name_for_user(self, user, new_middle_name):
        user_additional_data = self.user_additional_data_model.objects.get(user=user)
        user_additional_data.middle_name = new_middle_name
        user_additional_data.save()
    

    def get_middle_name_for_user(self, user):
        user_additional_data = self.user_additional_data_model.objects.get(user=user)
        return user_additional_data.middle_name