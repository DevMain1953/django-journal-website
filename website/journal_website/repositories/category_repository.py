from django.db.models.query import QuerySet

from ..models import Category, ScientificPublication


class CategoryRepository:
    def __init__(self):
        self.__category_model = Category

    def get_category_by_id(self, id: int) -> Category:
        return self.__category_model.objects.get(pk=id)
    
    def get_all_categories_in_current_scientific_publication(self, current_scientific_publication: ScientificPublication) -> QuerySet:
        return self.__category_model.objects.filter(scientific_publication = current_scientific_publication)
