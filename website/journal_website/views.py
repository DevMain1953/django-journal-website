from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from .forms import UserRegistrationForm, UserAdditionalDataForm, ArticleForm
from .services import EmailService
from .managers import FileManager
from .repositories import UserAdditionalDataRepository, ArticleRepository, ScientificPublicationRepository, VolumeRepository, CategoryRepository, UserRepository

email_service = EmailService.EmailService()
file_manager = FileManager.FileManager()

user_additional_data = UserAdditionalDataRepository.UserAdditionalDataRepository()
article = ArticleRepository.ArticleRepository()
scientific_publication = ScientificPublicationRepository.ScientificPublicationRepository()
volume = VolumeRepository.VolumeRepository()
category = CategoryRepository.CategoryRepository()
user = UserRepository.UserRepository()


def display_homepage(request):
    return render(request, "static_pages/homepage.html")


def display_page_with_articles(request, number_of_page):
	pagination_for_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_articles(), number_of_articles_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "article/articles.html", {'pagination_for_articles': pagination_for_articles})


@login_required
def display_page_with_scientific_publications(request, number_of_page):
	pagination_for_scientific_publications = scientific_publication.get_pagination_for_list_of_scientific_publications(list_of_scientific_publications=scientific_publication.get_all_scientific_publications(), number_of_scientific_publications_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "scientific_publication/scientific_publications.html", {'pagination_for_scientific_publications': pagination_for_scientific_publications})


@login_required
def display_page_with_articles_for_specific_user(request, number_of_page):
	pagination_for_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_articles_for_user(request.user), number_of_articles_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "article/articles_for_specific_user.html", {'pagination_for_articles': pagination_for_articles})


@login_required
def add_new_article(request, pk_of_scientific_publication):
	current_scientific_publication = scientific_publication.get_scientific_publication_by_id(pk_of_scientific_publication)
	volumes = volume.get_all_volumes_in_current_scientific_publication(current_scientific_publication)
	categories = category.get_all_categories_in_current_scientific_publication(current_scientific_publication)
	if request.method == 'POST':
		filled_article_creation_form = ArticleForm(volumes, categories, request.POST, request.FILES)
		if filled_article_creation_form.is_valid():
			selected_volume_id = filled_article_creation_form.cleaned_data["volumes"]
			selected_category_id = filled_article_creation_form.cleaned_data["categories"]
			selected_file_name = request.FILES["file"].name

			unique_file_name = file_manager.save_file_to_server(selected_file_name, request.FILES["file"])

			volume_by_id = volume.get_volume_by_id(selected_volume_id)
			category_by_id = category.get_category_by_id(selected_category_id)
			article.add_new_article(file_name=unique_file_name, user=request.user, volume=volume_by_id, category=category_by_id)
			return redirect("specific_user_articles_with_pagination", number_of_page=1)
		else:
			messages.error(request, 'Form is invalid! Read hints')
	article_creation_form = ArticleForm(volumes, categories)
	return render(request, 'article/adding_new_article.html', {'article_creation_form': article_creation_form})


@login_required
def update_article(request, pk_of_article):
	current_article = article.get_article_by_id_and_user(pk_of_article, request.user)
	if current_article is None:
		return HttpResponse("There is no article with such id")
	current_scientific_publication = scientific_publication.get_scientific_publication_by_id(current_article.category.scientific_publication.pk)
	volumes = volume.get_all_volumes_in_current_scientific_publication(current_scientific_publication)
	categories = category.get_all_categories_in_current_scientific_publication(current_scientific_publication)
	if request.method == 'POST':
		filled_article_updating_form = ArticleForm(volumes, categories, request.POST, request.FILES)
		if filled_article_updating_form.is_valid():
			selected_volume_id = filled_article_updating_form.cleaned_data["volumes"]
			selected_category_id = filled_article_updating_form.cleaned_data["categories"]
			selected_file_name = request.FILES["file"].name

			unique_file_name = file_manager.save_file_to_server(selected_file_name, request.FILES["file"])
			file_manager.remove_file_from_server_by_name(current_article.file_name)

			volume_by_id = volume.get_volume_by_id(selected_volume_id)
			category_by_id = category.get_category_by_id(selected_category_id)
			article.update_article_by_id(id=pk_of_article, file_name=unique_file_name, volume=volume_by_id, category=category_by_id)
			return redirect("specific_user_articles_with_pagination", number_of_page=1)
	article_updating_form = ArticleForm(volumes, categories, initial={"volumes": current_article.volume.pk, "categories": current_article.category.pk})
	return render(request, 'article/updating_article.html', {'article_updating_form': article_updating_form})


@login_required
def display_remove_article_page(request, pk_of_article):
	if article.get_article_by_id_and_user(pk_of_article, request.user) is None:
		return HttpResponse("There is no article with such id")
	return render(request, 'article/removing_article.html', {'pk_of_article': pk_of_article})


@login_required
def remove_article(request, pk_of_article):
	if article.get_article_by_id_and_user(pk_of_article, request.user) is None:
		return HttpResponse("There is no article with such id")
	file_manager.remove_file_from_server_by_name(article.get_article_by_id(pk_of_article).file_name)
	article.remove_article_by_id(pk_of_article)
	return redirect("specific_user_articles_with_pagination", number_of_page=1)


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
		user_additional_data_by_code = user_additional_data.get_object_by_code(code=code)
		registered_user = User.objects.get(pk=user_additional_data_by_code.user.pk)
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
			new_user_additional_data = user_additional_data.add_new(new_user)
			email_service.send_email_message(sender="admin@example.com", receiver=new_user, subject="Account activation",
				   email_template_name="user/account_activation/account_activation_email.txt", code=new_user_additional_data.code)
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