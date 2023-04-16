from hmac import new
from ..models import String


class StringRepository:
    def __init__(self):
        self.__string_model = String
    

    def add_new_string(self, russian, english=""):
        new_string = self.__string_model(russian=russian, english=english)
        new_string.save()
        return new_string
