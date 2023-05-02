from django.test import TestCase

from ..repositories import StringRepository
from ..models import ScientificPublication, StaticPage, Category, ScientificSpecialty


string_repository = StringRepository.StringRepository()


class NewCategoryCreatingTest(TestCase):
    def setUp(self):
        new_name_of_scientific_publication = string_repository.add_new_string("Научное издание", "Scientific publication")
        new_name_of_scientific_specialty = string_repository.add_new_string("Научная специальность", "Scientific specialty")
        new_name_of_static_page = string_repository.add_new_string("Статическая страница", "Static page")
        new_name_of_category = string_repository.add_new_string("Первая категория", "First category")
        new_static_page = StaticPage.objects.create(name=new_name_of_static_page, relative_url_address="test_url")
        new_scientific_publication = ScientificPublication.objects.create(full_name=new_name_of_scientific_publication, short_name=new_name_of_scientific_publication, contacts=new_static_page,
                                             main_editor=new_static_page, legal_information=new_static_page, contract_information=new_static_page, science_branches=new_static_page,
                                             editorial_team=new_static_page)
        new_scientific_specialty = ScientificSpecialty.objects.create(name=new_name_of_scientific_specialty, science_branches=new_static_page)
        Category.objects.create(name=new_name_of_category, scientific_specialty=new_scientific_specialty, scientific_publication=new_scientific_publication)


    def test_newly_created_category(self):
        self.assertEqual(Category.objects.get(pk=1).name.russian, "Первая категория")
        self.assertEqual(Category.objects.get(pk=1).name.english, "First category")