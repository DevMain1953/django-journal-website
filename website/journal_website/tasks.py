from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from uuid import UUID


@shared_task
def send_email_message_to_user_with_activation_link(target_user_id: int, code: UUID) -> HttpResponse | None:
    target_user = User.objects.get(pk=target_user_id)
    content = {
        "email": target_user.email,
        "domain": "127.0.0.1:8000",
		"site_name": "Website",
        "user": target_user,
		"protocol": "http",
        "code": code,
    }

    message = render_to_string("user/account_activation/account_activation_email.txt", content)
    try:
        send_mail("Account activation", message, "admin@example.com" , [target_user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")


@shared_task
def send_email_message_to_user_with_password_reset_link(target_user_id: int) -> HttpResponse | None:
    target_user = User.objects.get(pk=target_user_id)
    content = {
        "email": target_user.email,
        "domain": "127.0.0.1:8000",
		"site_name": "Website",
        "user": target_user,
		"protocol": "http",
        "uid": urlsafe_base64_encode(force_bytes(target_user.pk)),
        "token": default_token_generator.make_token(target_user)
    }

    message = render_to_string("authentication/password/password_reset_email.txt", content)
    try:
        send_mail("Password Reset Requested", message, "admin@example.com" , [target_user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")


@shared_task
def send_notification_email_to_user(target_user_id: int, sender_id: int, id_of_article: int) -> HttpResponse | None:
    target_user = User.objects.get(pk=target_user_id)
    sender = User.objects.get(pk=sender_id)
    content = {
        "email": target_user.email,
        "domain": "127.0.0.1:8000",
		"site_name": "Website",
        "user": target_user,
		"protocol": "http",
        "id_of_article": id_of_article
    }
        
    message = render_to_string("feedback/new_feedback_email.txt", content)
    try:
        send_mail("There is new feedback to your article", message, sender.email , [target_user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")