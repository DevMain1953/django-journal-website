from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_main_page),
    path('registration/', views.display_registration_page),
    path('create/', views.create_user)
]
