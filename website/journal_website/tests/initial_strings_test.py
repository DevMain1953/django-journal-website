from django.test import TestCase

from ..repositories import StringRepository
from ..models import String


string_repository = StringRepository.StringRepository()


class InitialStringsTest(TestCase):
    def setUp(self):
        string_repository.add_new_string("Научное издание", "Scientific publication")
        string_repository.add_new_string("Научная специальность", "Scientific specialty")
        string_repository.add_new_string("Статическая страница", "Static page")
        string_repository.add_new_string("Раздел 1", "Volume 1")
        string_repository.add_new_string("Категория 1", "Category 1")
    
    def test_newly_created_strings(self):
        name_of_scientific_publication = String.objects.get(pk=1)
        name_of_scientific_specialty = String.objects.get(pk=2)
        name_of_static_page = String.objects.get(pk=3)
        name_of_volume = String.objects.get(pk=4)
        name_of_category = String.objects.get(pk=5)

        self.assertEqual(name_of_scientific_publication.russian, "Научное издание")
        self.assertEqual(name_of_scientific_publication.english, "Scientific publication")

        self.assertEqual(name_of_scientific_specialty.russian, "Научная специальность")
        self.assertEqual(name_of_scientific_specialty.english, "Scientific specialty")

        self.assertEqual(name_of_static_page.russian, "Статическая страница")
        self.assertEqual(name_of_static_page.english, "Static page")

        self.assertEqual(name_of_volume.russian, "Раздел 1")
        self.assertEqual(name_of_volume.english, "Volume 1")

        self.assertEqual(name_of_category.russian, "Категория 1")
        self.assertEqual(name_of_category.english, "Category 1")