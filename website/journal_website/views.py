from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from .forms import UserRegistrationForm, UserAdditionalDataForm
from .models import UserAdditionalData, Article
from .services import EmailService
from .repositories import UserAdditionalDataRepository, ArticleRepository

email_service = EmailService.EmailService()
user_additional_data = UserAdditionalDataRepository.UserAdditionalDataRepository(UserAdditionalData)
article = ArticleRepository.ArticleRepository(Article)


def display_homepage(request):
    return render(request, "static_pages/homepage.html")


def display_page_with_articles(request, number_of_page):
	pagination_for_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_articles(), number_of_articles_per_page=10, number_of_page_to_display=number_of_page)
	return render(request, "user/articles.html", {'pagination_for_articles': pagination_for_articles})


@login_required
def change_user_additional_data(request):
	if request.method == 'POST':
		filled_user_additional_data_form = UserAdditionalDataForm(request.POST)
		if filled_user_additional_data_form.is_valid():
			user_additional_data.save_middle_name_for_user(user=request.user, new_middle_name=filled_user_additional_data_form.cleaned_data['middle_name'])
			return redirect("homepage")
		else:
			messages.error(request, 'Form is invalid!')
	user_additional_data_form = UserAdditionalDataForm(instance=user_additional_data.get_object_by_user(user=request.user))
	return render(request, 'user/account_settings.html', {'user_additional_data_form': user_additional_data_form})


def activate_user_account(request, code):
	try:
		user_additional_data = UserAdditionalData.objects.get(code=code)
		registered_user = User.objects.get(pk=user_additional_data.user.pk)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		registered_user = None
	if registered_user is not None:
		registered_user.is_active = True
		registered_user.save()
		return HttpResponse('Thank you for your account activation. Now you can <a href="/authorization">login</a>.')
	else:
		return HttpResponse('Activation link is invalid!')


@login_required
def change_user_password(request):
	if request.method == 'POST':
		filled_password_change_form = PasswordChangeForm(request.user, request.POST)
		if filled_password_change_form.is_valid():
			user_with_new_password = filled_password_change_form.save()
			update_session_auth_hash(request, user_with_new_password)
			return HttpResponse('Your password successfully changed. <a href="/">Go home</a>')
		else:
			messages.error(request, 'Please make sure that you entered correct password while confirmation and old password is correct too.')
	password_change_form = PasswordChangeForm(request.user)
	return render(request, 'user/change_password.html', {'password_change_form': password_change_form})


def register_new_user(request):
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		filled_registration_form = UserRegistrationForm(request.POST)
		if filled_registration_form.is_valid():
			new_user = filled_registration_form.save()
			user_additional_data = UserAdditionalData.objects.create(user=new_user)
			email_service.send_email_message(sender="admin@example.com", receiver=new_user, subject="Account activation",
				   email_template_name="user/account_activation/account_activation_email.txt", code=user_additional_data.code)
			return HttpResponse('We sent email with instructions to activate your account. <a href="/">Go home</a>')
		else:
			messages.error(request, "Unsuccessful registration. Please read all hints under input fields. Hint: maybe username you entered is already in use!")
	registration_form = UserRegistrationForm()
	return render(request=request, template_name="authentication/registration.html", context={"registration_form": registration_form})


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
	return render(request=request, template_name="authentication/authorization.html", context={"authorization_form": authorization_form})


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
					email_service.send_email_message(sender="admin@example.com", receiver=user, subject="Password Reset Requested",
				     email_template_name="authentication/password/password_reset_email.txt")
					return redirect ("/password_reset/done/")
		messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form": password_reset_form})