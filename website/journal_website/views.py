from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import UserRegistrationForm
from .models import UserAdditionalData
from .services.email import EmailService


def display_homepage(request):
    return render(request, "static_pages/homepage.html")


@login_required
def display_account_settings_page(request):
	return render(request, "user/account_settings.html")


def activate_user_account(request, uidb64, token):
	try:
		uid = force_bytes(urlsafe_base64_decode(uidb64))
		registered_user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		registered_user = None
	if registered_user is not None and default_token_generator.check_token(registered_user, token):
		registered_user.is_active = True
		registered_user.save()
		return HttpResponse('Thank you for your account activation. Now you can <a href="/authorization">login</a>.')
	else:
		return HttpResponse('Activation link is invalid!')


def register_new_user(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		filled_registration_form = UserRegistrationForm(request.POST)
		if filled_registration_form.is_valid():
			new_user = filled_registration_form.save()
			UserAdditionalData.objects.create(user=new_user)
			EmailService.send_email_message(sender="admin@example.com", receiver=new_user, subject="Account activation",
				   email_template_name="user/account_activation/account_activation_email.txt")
			return HttpResponse('We sent email with instructions to activate your account. <a href="/">Go home</a>')
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
			authenticated_user = authenticate(username=username, password=password)
			if authenticated_user is not None:
				login(request, authenticated_user)
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	authorization_form = AuthenticationForm()
	return render(request=request, template_name="authentication/authorization.html", context={"authorization_form":authorization_form})


@login_required
def logout_user(request):
	logout(request)
	return redirect("homepage")


def reset_password(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		filled_password_reset_form = PasswordResetForm(request.POST)
		if filled_password_reset_form.is_valid():
			user_email = filled_password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=user_email))
			if associated_users.exists():
				for user in associated_users:
					EmailService.send_email_message(sender="admin@example.com", receiver=user, subject="Password Reset Requested",
				     email_template_name="authentication/password/password_reset_email.txt")
					return redirect ("/password_reset/done/")
		messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form":password_reset_form})