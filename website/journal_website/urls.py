from django.urls import path
from . import views

urlpatterns = [
    path("", views.display_homepage, name="homepage"),
    path("account_settings", views.change_user_additional_data, name="account_settings"),
    path("password_change", views.change_user_password, name="password_change"),
    path("articles/<int:number_of_page>", views.display_page_with_articles, name="articles_with_pagination"),
    path("my_articles/<int:number_of_page>", views.display_page_with_articles_for_specific_user, name="specific_user_articles_with_pagination"),
    path("scientific_publications/<int:number_of_page>", views.display_page_with_scientific_publications, name="scientific_publications_with_pagination"),

    path("scientific_publication/<int:pk_of_scientific_publication>/add_article", views.add_new_article, name="add_article_to_scientific_publication"),
    path("article/<int:pk_of_article>/update", views.update_article, name="update_article"),
    path("article/<int:pk_of_article>/delete", views.display_remove_article_page, name="delete_article"),
    path("article/<int:pk_of_article>/remove", views.remove_article, name="remove_article"),
    
    path("account_activation/<code>/", views.activate_user_account, name="account_activation"),

    path("registration", views.register_new_user, name="registration"),
    path("authorization", views.authorize_user, name="authorization"),
    path("logout", views.logout_user, name= "logout"),
    path("password_reset", views.reset_password, name="password_reset")
]