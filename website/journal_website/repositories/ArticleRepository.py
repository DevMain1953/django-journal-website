from django.core.paginator import Paginator
from datetime import datetime

from . import StringRepository
from ..models import Article


class ArticleRepository:
    def __init__(self):
        self.__article_model = Article
        self.__string = StringRepository.StringRepository()


    def get_all_articles(self):
        return self.__article_model.objects.all().order_by("pk")
    

    def get_all_articles_for_user(self, user):
        return self.__article_model.objects.filter(user=user)
    

    def get_pagination_for_list_of_articles(self, list_of_articles, number_of_articles_per_page, number_of_page_to_display):
        paginator = Paginator(list_of_articles, per_page=number_of_articles_per_page)
        return paginator.get_page(number_of_page_to_display)
    

    def add_new_article(self, file_name, user, volume, category):
        #TODO: add doxc file parsing intead of this: 
        new_article_name = self.__string.add_new_string("Новая статья")
        new_short_description = self.__string.add_new_string("Новое короткое описание")
        new_article = self.__article_model(name=new_article_name, short_description=new_short_description, publication_date=datetime.now(),
                                         file_name=file_name, authors="authors", user=user, volume=volume, category=category)
        #end
        new_article.save()
        return new_article
    

    def get_article_by_id(self, id):
        return self.__article_model.objects.get(pk=id)
    

    def get_article_by_id_and_user(self, id, user):
        return self.__article_model.objects.filter(pk=id, user=user).first()
    

    def update_article_by_id(self, id, file_name, volume, category):
        #TODO: add parsing here as well
        current_article = self.__article_model.objects.get(pk=id)
        current_article.file_name = file_name
        current_article.volume = volume
        current_article.category = category
        #end
        current_article.save()
    

    def remove_article_by_id(self, id):
        current_article = self.__article_model.objects.get(pk=id)
        current_article.delete()

