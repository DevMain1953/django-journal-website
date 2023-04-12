from django.urls import path
from . import views

urlpatterns = [
    path("", views.display_homepage, name="homepage"),
    path("account_settings", views.change_user_additional_data, name="account_settings"),
    path("password_change", views.change_user_password, name="password_change"),
    path("articles/<int:number_of_page>", views.display_page_with_articles, name="articles_with_pagination"),
    
    path("account_activation/<code>/", views.activate_user_account, name="account_activation"),

    path("registration", views.register_new_user, name="registration"),
    path("authorization", views.authorize_user, name="authorization"),
    path("logout", views.logout_user, name= "logout"),
    path("password_reset", views.reset_password, name="password_reset")
]