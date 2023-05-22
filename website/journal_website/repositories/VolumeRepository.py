from ..models import Volume, ScientificPublication

from django.db.models.query import QuerySet


class VolumeRepository:
    def __init__(self):
        self.__volume_model = Volume

    def get_volume_by_id(self, id: int) -> Volume:
        return self.__volume_model.objects.get(pk=id)
    
    def get_all_volumes_in_current_scientific_publication(self, current_scientific_publication: ScientificPublication) -> QuerySet:
        return self.__volume_model.objects.filter(scientific_publication = current_scientific_publication)
