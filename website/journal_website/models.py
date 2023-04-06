from django.db import models
import uuid

class String(models.Model):
    russian = models.TextField()
    english = models.TextField()

    class Meta:
        verbose_name_plural = 'strings'

class StaticPage(models.Model):
    name = models.ForeignKey(String, related_name='static_pages', on_delete=models.CASCADE)
    relative_url_address = models.TextField()

    class Meta:
        verbose_name_plural = 'static_pages'

class ScientificPublication(models.Model):
    full_name = models.ForeignKey(String, related_name='scientific_publications', on_delete=models.CASCADE)
    short_name = models.ForeignKey(String, related_name='scientific_publications', on_delete=models.CASCADE)
    contacts = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)
    main_editor = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)
    legal_information = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)
    contract_information = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)
    science_branches = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)
    editorial_team = models.ForeignKey(StaticPage, related_name='scientific_publications', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'scientific_publications'

class Volume(models.Model):
    name = models.ForeignKey(String, related_name='volumes', on_delete=models.CASCADE)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='volumes', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'volumes'

class ScientificSpecialty(models.Model):
    name = models.ForeignKey(String, related_name='scientific_specialties', on_delete=models.CASCADE)
    science_branches = models.ForeignKey(StaticPage, related_name='scientific_specialties', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'scientific_specialties'  

class Category(models.Model):
    name = models.ForeignKey(String, related_name='categories', on_delete=models.CASCADE)
    scientific_specialty = models.ForeignKey(ScientificSpecialty, related_name='categories', on_delete=models.DO_NOTHING)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='categories', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'categories'

class Founder(models.Model):
    full_name = models.ForeignKey(String, on_delete=models.CASCADE)
    scientific_publication = models.ForeignKey(ScientificPublication, related_name='founders', on_delete=models.DO_NOTHING)
    contacts = models.ForeignKey(StaticPage, related_name='founders', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'founders'

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.TextField()
    password = models.TextField()
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name_plural = 'users'

class Article(models.Model):
    name = models.ForeignKey(String, related_name='articles', on_delete=models.CASCADE)
    short_description = models.ForeignKey(String, related_name='articles', on_delete=models.CASCADE)
    publication_date = models.DateField()
    file_name = models.TextField()
    authors = models.TextField()
    user = models.ForeignKey(User, related_name='articles', on_delete=models.DO_NOTHING)
    volume = models.ForeignKey(Volume, related_name='articles', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'articles'

class Feedback(models.Model):
    comment = models.TextField()
    article = models.ForeignKey(Article, related_name='feedbacks', on_delete=models.CASCADE)
    publication_date = models.DateField()
    decision = models.CharField(max_length=20, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected')])

    class Meta:
        verbose_name_plural = 'feedbacks'