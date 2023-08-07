from django.urls import path
from . import views

urlpatterns = [
    path("", views.display_homepage, name="homepage"),
    path("account-settings", views.change_user_additional_data, name="account_settings"),
    path("password-change", views.change_user_password, name="password_change"),
    path("articles/<int:number_of_page>", views.display_page_with_articles, name="articles_with_pagination"),
    path("accepted-articles/<int:number_of_page>", views.display_page_with_accepted_articles, name="accepted_articles_with_pagination"),
    path("scientific-publications/<int:number_of_page>", views.display_page_with_scientific_publications, name="scientific_publications_with_pagination"),

    path("my-articles/<int:number_of_page>", views.display_page_with_articles_for_specific_user, name="specific_user_articles_with_pagination"),
    path("scientific-publication/<int:pk_of_scientific_publication>/add-article", views.add_article, name="add_article_to_scientific_publication"),
    path("article/<int:pk_of_article>/update", views.update_article, name="update_article"),
    path("article/<int:pk_of_article>/delete", views.display_remove_article_page, name="delete_article"),
    path("article/<int:pk_of_article>/remove", views.remove_article, name="remove_article"),
    path("article/<int:pk_of_article>/details", views.display_article_with_feedbacks, name="article_details"),
    path("article/<int:pk_of_article>/download", views.download_article, name="article_download"),

    path("my-feedbacks/<int:number_of_page>/", views.display_page_with_feedbacks_for_specific_user, name="specific_user_feedbacks_with_pagination"),
    path("article/<int:pk_of_article>/add-feedback", views.add_feedback, name="add_feedback_to_article"),
    path("feedback/<int:pk_of_feedback>/update", views.update_feedback, name="update_feedback"),
    path("feedback/<int:pk_of_feedback>/delete", views.display_remove_feedback_page, name="delete_feedback"),
    path("feedback/<int:pk_of_feedback>/remove", views.remove_feedback, name="remove_feedback"),
    
    path("account-activation/<str:code>/", views.activate_user_account, name="account_activation"),

    path("registration", views.register_new_user, name="registration"),
    path("authorization", views.authorize_user, name="authorization"),
    path("logout", views.logout_user, name= "logout"),
    path("password-reset", views.reset_password, name="password_reset")
]