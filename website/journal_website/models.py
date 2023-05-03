from django.contrib.auth.models import User
from django.db import models
import uuid


class String(models.Model):
    russian = models.TextField()
    english = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.english


    class Meta:
        verbose_name_plural = 'strings'


class StaticPage(models.Model):
    name = models.ForeignKey(String, related_name='static_page_name', on_delete=models.CASCADE)
    relative_url_address = models.TextField()

    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = 'static_pages'


class ScientificPublication(models.Model):
    full_name = models.ForeignKey(String, related_name='scientific_publication_full_name', on_delete=models.CASCADE)
    short_name = models.ForeignKey(String, related_name='scientific_publication_short_name', on_delete=models.CASCADE)
    contacts = models.ForeignKey(StaticPage, related_name='scientific_publication_contacts', on_delete=models.SET_NULL, null=True)
    main_editor = models.ForeignKey(StaticPage, related_name='scientific_publication_main_editor', on_delete=models.SET_NULL, null=True)
    legal_information = models.ForeignKey(StaticPage, related_name='scientific_publication_legal_information', on_delete=models.SET_NULL, null=True)
    contract_information = models.ForeignKey(StaticPage, related_name='scientific_publication_contract_information', on_delete=models.SET_NULL, null=True)
    science_branches = models.ForeignKey(StaticPage, related_name='scientific_publication_science_branches', on_delete=models.SET_NULL, null=True)
    editorial_team = models.ForeignKey(StaticPage, related_name='scientific_publication_editorial_team', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.short_name)
    

    class Meta:
        verbose_name_plural = 'scientific_publications'


class Volume(models.Model):
    name = models.ForeignKey(String, related_name='volume_name', on_delete=models.CASCADE)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='volume_scientific_publication', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = 'volumes'


class ScientificSpecialty(models.Model):
    name = models.ForeignKey(String, related_name='scientific_specialty_name', on_delete=models.CASCADE)
    science_branches = models.ForeignKey(StaticPage, related_name='scientific_specialty_science_branches', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = 'scientific_specialties'  


class Category(models.Model):
    name = models.ForeignKey(String, related_name='category_name', on_delete=models.CASCADE)
    scientific_specialty = models.ForeignKey(ScientificSpecialty, related_name='category_scientific_specialty', on_delete=models.CASCADE)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='category_scientific_publication', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = 'categories'


class Founder(models.Model):
    full_name = models.ForeignKey(String, related_name='founder_full_name', on_delete=models.CASCADE)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='founder_scientific_publication', on_delete=models.CASCADE)
    contacts = models.ForeignKey(StaticPage, related_name='founder_contacts', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.full_name)
    

    class Meta:
        verbose_name_plural = 'founders'


class UserAdditionalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return str(self.user)
    

    class Meta:
        verbose_name_plural = 'user_additional_data'


class Article(models.Model):
    name = models.ForeignKey(String, related_name='article_name', on_delete=models.CASCADE)
    short_description = models.ForeignKey(String, related_name='article_short_description', on_delete=models.CASCADE)
    publication_date = models.DateField()
    file_name = models.TextField()
    authors = models.ForeignKey(String, related_name='article_authors', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='article_custom_user', on_delete=models.SET_NULL, null=True)
    volume = models.ForeignKey(Volume, related_name='article_volume', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='article_category', on_delete=models.SET_NULL, null=True)
    DECISIONS = [('accepted', 'Accepted'), ('rejected', 'Rejected'), ('awaiting_decision', 'Awaiting decision')]
    decision = models.CharField(max_length=20, choices=DECISIONS)


    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = 'articles'


class Feedback(models.Model):
    comment = models.TextField()
    article = models.ForeignKey(Article, related_name='feedback_article', on_delete=models.CASCADE)
    publication_date = models.DateField()
    user = models.ForeignKey(User, related_name='feedback_custom_user', on_delete=models.SET_NULL, null=True)
    DECISIONS = [('accepted', 'Accepted'), ('rejected', 'Rejected')]
    decision = models.CharField(max_length=20, choices=DECISIONS)


    def __str__(self):
        return str(self.article)
    

    class Meta:
        verbose_name_plural = 'feedbacks'