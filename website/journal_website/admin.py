from django.contrib import admin

from .models import String, StaticPage, ScientificPublication, Volume, ScientificSpecialty, Category, Founder, UserAdditionalData, Article, Feedback

admin.site.register(String)
admin.site.register(StaticPage)
admin.site.register(ScientificPublication)
admin.site.register(Volume)
admin.site.register(ScientificSpecialty)
admin.site.register(Category)
admin.site.register(Founder)
admin.site.register(UserAdditionalData)
admin.site.register(Article)
admin.site.register(Feedback)