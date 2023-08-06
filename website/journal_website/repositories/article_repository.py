from django.core.paginator import Paginator, Page
from django.db.models.query import QuerySet
from django.utils.functional import SimpleLazyObject
from datetime import datetime

from .string_repository import StringRepository
from ..models import Article, Volume, Category


class ArticleRepository:
    def __init__(self):
        self.__article_model = Article
        self.__string = StringRepository()

    def get_all_articles(self) -> QuerySet:
        return self.__article_model.objects.all().order_by("pk")
    
    def get_all_accepted_articles(self) -> QuerySet:
        return self.__article_model.objects.filter(decision="accepted")

    def get_all_articles_for_user(self, user: SimpleLazyObject) -> QuerySet:
        return self.__article_model.objects.filter(user=user)
    
    def get_pagination_for_list_of_articles(self, list_of_articles: QuerySet, number_of_articles_per_page: int, number_of_page_to_display: int) -> Page:
        paginator = Paginator(list_of_articles, per_page=number_of_articles_per_page)
        return paginator.get_page(number_of_page_to_display)
    
    def add_new_article(self, name: str, short_description: str, file_name: str, authors: str, user: SimpleLazyObject, volume: Volume, category: Category, decision: str) -> Article:
        new_article_name = self.__string.add_new_string(name)
        new_short_description = self.__string.add_new_string(short_description)
        new_authors = self.__string.add_new_string(authors)
        new_article = self.__article_model(name=new_article_name, short_description=new_short_description, publication_date=datetime.now(),
                                         file_name=file_name, authors=new_authors, user=user, volume=volume, category=category, decision=decision)
        new_article.save()
        return new_article
    
    def update_decision_for_article_by_id(self, id: int, decision: str):
        current_article = self.get_article_by_id(id)
        current_article.decision = decision
        current_article.save()

    def get_article_by_id(self, id: int) -> Article:
        return self.__article_model.objects.get(pk=id)
    
    def get_article_by_id_and_user(self, id: int, user: SimpleLazyObject) -> Article | None:
        return self.__article_model.objects.filter(pk=id, user=user).first()
    
    def update_article_by_id(self, id: int, name: str, short_description: str, file_name: str, authors: str, volume: Volume, category: Category):
        current_article = self.__article_model.objects.get(pk=id)
        self.__string.update_string_by_id(current_article.name.pk, name)
        self.__string.update_string_by_id(current_article.short_description.pk, short_description)
        self.__string.update_string_by_id(current_article.authors.pk, authors)

        current_article.file_name = file_name
        current_article.volume = volume
        current_article.category = category
        current_article.save()
    
    def add_foreign_language_to_article_by_id(self, id: int, name: str, short_description: str, authors: str):    
        current_article = self.__article_model.objects.get(pk=id)

        self.__string.update_string_by_id(current_article.name.pk, current_article.name.russian, name)
        self.__string.update_string_by_id(current_article.short_description.pk, current_article.short_description.russian, short_description)
        self.__string.update_string_by_id(current_article.authors.pk, current_article.authors.russian, authors)

        current_article.save()
    
    def remove_article_by_id(self, id: int):
        current_article = self.__article_model.objects.get(pk=id)
        id_of_article_name = current_article.name.pk
        id_of_article_short_description = current_article.short_description.pk
        id_of_article_authors = current_article.authors.pk

        current_article.delete()
        
        self.__string.remove_string_by_id(id_of_article_name)
        self.__string.remove_string_by_id(id_of_article_short_description)
        self.__string.remove_string_by_id(id_of_article_authors)

