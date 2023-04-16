from django.core.paginator import Paginator
from ..models import Feedback
from datetime import datetime


class FeedbackRepository:
    def __init__(self):
        self.__feedback_model = Feedback


    def get_feedback_by_id(self, id):
        return self.__feedback_model.objects.get(pk=id)
    

    def get_feedback_by_id_and_user(self, id, user):
        return self.__feedback_model.objects.filter(pk=id, user=user).first()
    
    
    def get_all_feedbacks_for_user(self, user):
        return self.__feedback_model.objects.filter(user = user)
    

    def get_pagination_for_list_of_feedbacks(self, list_of_feedbacks, number_of_feedbacks_per_page, number_of_page_to_display):
        paginator = Paginator(list_of_feedbacks, per_page=number_of_feedbacks_per_page)
        return paginator.get_page(number_of_page_to_display)
    

    def add_new_feedback(self, comment, article, user, decision):
        new_feedback = self.__feedback_model(comment=comment, article=article, publication_date=datetime.now(), user=user, decision=decision)
        new_feedback.save()
        return new_feedback
    

    def remove_feedback_by_id(self, id):
        current_feedback = self.__feedback_model.objects.get(pk=id)
        current_feedback.delete()

    
    def update_feedback_by_id(self, id, comment, decision):
        current_feedack = self.__feedback_model.objects.get(pk=id)
        current_feedack.comment = comment
        current_feedack.decision = decision
        current_feedack.save()

    
    def get_decisions(self):
        return self.__feedback_model.DECISIONS
