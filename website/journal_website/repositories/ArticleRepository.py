from django.core.paginator import Paginator


class ArticleRepository:
    def __init__(self, model):
        self.article_model = model


    def get_all_articles(self):
        return self.article_model.objects.all().order_by("pk")
    

    def get_pagination_for_list_of_articles(self, list_of_articles, number_of_articles_per_page, number_of_page_to_display):
        paginator = Paginator(list_of_articles, per_page=number_of_articles_per_page)
        return paginator.get_page(number_of_page_to_display)
