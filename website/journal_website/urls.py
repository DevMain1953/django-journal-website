from django.urls import path
from . import views

urlpatterns = [
    path("", views.display_homepage, name="homepage"),
    path("registration", views.register_new_user, name="registration"),
    path("authorization", views.authorize_user, name="authorization"),
    path("logout", views.logout_user, name= "logout"),
    path("password_reset", views.reset_password, name="password_reset")
]