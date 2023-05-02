from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


class FileManager:
    def __init__(self):
        self.__file_system_storage = FileSystemStorage()
    
    
    def save_file_to_server(self, file_name: str, file: InMemoryUploadedFile) -> str:
        file_extenshion = file_name.split(".")[1]
        new_file_name = str(str(uuid.uuid4()) + "." + file_extenshion)
        return self.__file_system_storage.save(new_file_name, file)
    

    def remove_file_from_server_by_name(self, file_name: str):
        if self.__file_system_storage.exists(file_name):
            self.__file_system_storage.delete(file_name)
        else:
            raise Exception("Couldn't find file")