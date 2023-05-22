from django.core.paginator import Paginator, Page
from django.utils.functional import SimpleLazyObject
from django.db.models.query import QuerySet
from datetime import datetime

from . import ArticleRepository
from ..models import Feedback, Article


class FeedbackRepository:
    def __init__(self):
        self.__feedback_model = Feedback
        self.__article = ArticleRepository.ArticleRepository()

    def get_feedback_by_id(self, id: int) -> Feedback:
        return self.__feedback_model.objects.get(pk=id)
    
    def get_feedback_by_id_and_user(self, id: int, user: SimpleLazyObject) -> Feedback | None:
        return self.__feedback_model.objects.filter(pk=id, user=user).first()
      
    def get_all_feedbacks_for_user(self, user: SimpleLazyObject) -> QuerySet:
        return self.__feedback_model.objects.filter(user=user)
    
    def get_pagination_for_list_of_feedbacks(self, list_of_feedbacks: QuerySet, number_of_feedbacks_per_page: int, number_of_page_to_display: int) -> Page:        
        paginator = Paginator(list_of_feedbacks, per_page=number_of_feedbacks_per_page)
        return paginator.get_page(number_of_page_to_display)
    
    def add_new_feedback(self, comment: str, article: Article, user: SimpleLazyObject, decision: str) -> Feedback:    
        new_feedback = self.__feedback_model(comment=comment, article=article, publication_date=datetime.now(), user=user, decision=decision)
        new_feedback.save()
        self.update_decision_for_article_based_on_ratio_of_accepted_and_rejected_feedback_decisions(article)
        return new_feedback
    
    def remove_feedback_by_id(self, id: int):
        current_feedback = self.__feedback_model.objects.get(pk=id)
        related_article = current_feedback.article
        current_feedback.delete()
        self.update_decision_for_article_based_on_ratio_of_accepted_and_rejected_feedback_decisions(related_article)

    def update_feedback_by_id(self, id: int, comment: str, decision: str):
        current_feedack = self.__feedback_model.objects.get(pk=id)
        current_feedack.comment = comment
        current_feedack.decision = decision
        current_feedack.save()
        
        self.update_decision_for_article_based_on_ratio_of_accepted_and_rejected_feedback_decisions(current_feedack.article)

    def get_decisions(self) -> list:
        return self.__feedback_model.DECISIONS
    
    def get_all_feedbacks_to_article(self, article: Article) -> QuerySet:
        return self.__feedback_model.objects.filter(article=article)
    
    def __get_number_of_feedbacks_to_article_with_specified_decision(self, article: Article, decision: str) -> int:
        return self.__feedback_model.objects.filter(article=article, decision=decision).count()
    
    def update_decision_for_article_based_on_ratio_of_accepted_and_rejected_feedback_decisions(self, article: Article):
        number_of_feedbacks_with_rejected_decision = self.__get_number_of_feedbacks_to_article_with_specified_decision(article, "rejected")
        number_of_feedbacks_with_accepted_decision = self.__get_number_of_feedbacks_to_article_with_specified_decision(article, "accepted")

        if number_of_feedbacks_with_accepted_decision > number_of_feedbacks_with_rejected_decision:
            self.__article.update_decision_for_article_by_id(id=article.pk, decision="accepted")
        if number_of_feedbacks_with_accepted_decision < number_of_feedbacks_with_rejected_decision:
            self.__article.update_decision_for_article_by_id(id=article.pk, decision="rejected")
        if number_of_feedbacks_with_accepted_decision == number_of_feedbacks_with_rejected_decision:
            self.__article.update_decision_for_article_by_id(id=article.pk, decision="awaiting_decision")
