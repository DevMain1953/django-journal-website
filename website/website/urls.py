from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("journal_website.urls")),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="authentication/password/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password/password_reset_complete.html"), name="password_reset_complete")
]
