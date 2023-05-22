from ..models import String


class StringRepository:
    def __init__(self):
        self.__string_model = String
    
    def add_new_string(self, russian: str, english: str = "") -> String:
        new_string = self.__string_model(russian=russian, english=english)
        new_string.save()
        return new_string
    
    def update_string_by_id(self, id: int, russian: str, english: str = ""):
        current_string = self.__string_model.objects.get(pk=id)
        current_string.russian = russian
        current_string.english = english
        current_string.save()
    
    def remove_string_by_id(self, id: int):
        current_string = self.__string_model.objects.get(pk=id)
        current_string.delete()
