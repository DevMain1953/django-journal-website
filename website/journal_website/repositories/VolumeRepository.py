from ..models import Volume


class VolumeRepository:
    def __init__(self):
        self.__volume_model = Volume


    def get_volume_by_id(self, id):
        return self.__volume_model.objects.get(pk=id)
    
    
    def get_all_volumes_in_current_scientific_publication(self, current_scientific_publication):
        return self.__volume_model.objects.filter(scientific_publication = current_scientific_publication)
