from django.shortcuts import  render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def display_homepage(request):
    return render(request, "static_pages/homepage.html")


def register_new_user(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		form_with_new_user_data = UserRegistrationForm(request.POST)
		if form_with_new_user_data.is_valid():
			form_with_new_user_data.save()
			return redirect("homepage")
		else:
			messages.error(request, "Unsuccessful registration. Please read all hints under input fields.")
	registration_form = UserRegistrationForm()
	return render(request=request, template_name="authentication/registration.html", context={"registration_form":registration_form})


def authorize_user(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		form_with_credentials = AuthenticationForm(request, data=request.POST)
		if form_with_credentials.is_valid():
			username = form_with_credentials.cleaned_data.get('username')
			password = form_with_credentials.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	authorization_form = AuthenticationForm()
	return render(request=request, template_name="authentication/authorization.html", context={"authorization_form":authorization_form})


def logout_user(request):
	logout(request)
	return redirect("homepage")


def reset_password(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			user_email = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=user_email))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "authentication/password/password_reset_email.txt"
					content = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					message = render_to_string(email_template_name, content)
					try:
						send_mail(subject, message, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form":password_reset_form})