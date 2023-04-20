from django.test import TestCase
from ..repositories import StringRepository
from ..models import String, ScientificPublication, StaticPage, Volume


string_repository = StringRepository.StringRepository()


class NewVolumeCreatingTest(TestCase):
    def setUp(self):
        new_name_of_scientific_publication = string_repository.add_new_string("Научное издание", "Scientific publication")
        new_name_of_static_page = string_repository.add_new_string("Статическая страница", "Static page")
        new_name_of_volume = string_repository.add_new_string("Первый раздел", "First volume")
        new_static_page = StaticPage.objects.create(name=new_name_of_static_page, relative_url_address="test_url")
        new_scientific_publication = ScientificPublication.objects.create(full_name=new_name_of_scientific_publication, short_name=new_name_of_scientific_publication, contacts=new_static_page,
                                             main_editor=new_static_page, legal_information=new_static_page, contract_information=new_static_page, science_branches=new_static_page,
                                             editorial_team=new_static_page)
        Volume.objects.create(name=new_name_of_volume, scientific_publication=new_scientific_publication)


    def test_newly_created_volume(self):
        self.assertEqual(Volume.objects.get(pk=1).name.russian, "Первый раздел")
        self.assertEqual(Volume.objects.get(pk=1).name.english, "First volume")