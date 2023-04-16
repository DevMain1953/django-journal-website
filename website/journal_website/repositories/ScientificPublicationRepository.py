from django.core.paginator import Paginator
from ..models import ScientificPublication


class ScientificPublicationRepository:
    def __init__(self):
        self.__scientific_publication_model = ScientificPublication


    def get_all_scientific_publications(self):
        return self.__scientific_publication_model.objects.all().order_by("pk")
    

    def get_pagination_for_list_of_scientific_publications(self, list_of_scientific_publications, number_of_scientific_publications_per_page, number_of_page_to_display):
        paginator = Paginator(list_of_scientific_publications, per_page=number_of_scientific_publications_per_page)
        return paginator.get_page(number_of_page_to_display)
    

    def get_scientific_publication_by_id(self, id):
        return self.__scientific_publication_model.objects.get(pk=id)