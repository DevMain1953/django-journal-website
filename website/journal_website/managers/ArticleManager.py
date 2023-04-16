from django.conf import settings


class ArticleManager:
    def __init__(self):
        pass
    
    
    def get_name_of_article_from_file(self, file_name):
        path_to_file = settings.MEDIA_ROOT + file_name