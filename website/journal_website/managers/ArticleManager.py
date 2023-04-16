from django.conf import settings
from docx import Document


class ArticleManager:
    def __init__(self):
        self.__docx_document_parser = Document
    

    def get_base_information_about_article_in_russian_from_file(self, file_name):
        base_information = {}
        number_of_paragraph = 0
        path_to_file = settings.MEDIA_ROOT + file_name
        document = self.__docx_document_parser(path_to_file)
        for paragraph in document.paragraphs:
            if paragraph.style.name == "Main Title":
                number_of_paragraph += 1
                if number_of_paragraph == 2:
                    base_information["name"] = paragraph.text
                if number_of_paragraph == 3:
                    base_information["short_description"] = paragraph.text
        number_of_paragraph = 0
        for paragraph in document.paragraphs:
            if paragraph.style.name == "University Name":
                number_of_paragraph += 1
                if number_of_paragraph == 1:
                    base_information["authors"] = paragraph.text
        return base_information
    

    def get_base_information_about_article_in_english_from_file(self, file_name):
        base_information = {}
        number_of_paragraph = 0
        path_to_file = settings.MEDIA_ROOT + file_name
        document = self.__docx_document_parser(path_to_file)
        for paragraph in document.paragraphs:
            if paragraph.style.name == "Main Title":
                number_of_paragraph += 1
                if number_of_paragraph == 4:
                    base_information["name"] = paragraph.text
                if number_of_paragraph == 5:
                    base_information["short_description"] = paragraph.text
        number_of_paragraph = 0
        for paragraph in document.paragraphs:
            if paragraph.style.name == "University Name":
                number_of_paragraph += 1
                if number_of_paragraph == 3:
                    base_information["authors"] = paragraph.text
        return base_information
