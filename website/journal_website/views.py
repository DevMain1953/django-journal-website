from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, FileResponse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from .forms import UserRegistrationForm, UserAdditionalDataForm, ArticleForm, FeedbackForm
from .managers import FileManager, ArticleManager
from .repositories import UserAdditionalDataRepository, ArticleRepository, ScientificPublicationRepository, VolumeRepository, CategoryRepository, UserRepository, FeedbackRepository
from .tasks import send_email_message_to_user_with_activation_link, send_email_message_to_user_with_password_reset_link, send_notification_email_to_user

file_manager = FileManager()
article_manager = ArticleManager()

user_additional_data = UserAdditionalDataRepository()
article = ArticleRepository()
scientific_publication = ScientificPublicationRepository()
volume = VolumeRepository()
category = CategoryRepository()
feedback = FeedbackRepository()
user = UserRepository()


def display_homepage(request: WSGIRequest) -> HttpResponse:
    return render(request, "static_pages/homepage.html")


@login_required
@user_passes_test(user.is_user_reviewer)
def display_page_with_articles(request: WSGIRequest, number_of_page: int) -> HttpResponse:
	pagination_for_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_articles(), number_of_articles_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "article/articles.html", {"pagination_for_articles": pagination_for_articles})


def display_page_with_accepted_articles(request: WSGIRequest, number_of_page: int) -> HttpResponse:
	pagination_for_accepted_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_accepted_articles(), number_of_articles_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "article/articles.html", {"pagination_for_articles": pagination_for_accepted_articles})


@login_required
def display_page_with_scientific_publications(request: WSGIRequest, number_of_page: int) -> HttpResponse:
	pagination_for_scientific_publications = scientific_publication.get_pagination_for_list_of_scientific_publications(list_of_scientific_publications=scientific_publication.get_all_scientific_publications(), number_of_scientific_publications_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "scientific_publication/scientific_publications.html", {"pagination_for_scientific_publications": pagination_for_scientific_publications})


@login_required
def display_page_with_articles_for_specific_user(request: WSGIRequest, number_of_page: int) -> HttpResponse:
	pagination_for_articles = article.get_pagination_for_list_of_articles(list_of_articles=article.get_all_articles_for_user(request.user), number_of_articles_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "article/articles_for_specific_user.html", {"pagination_for_articles": pagination_for_articles})


@login_required
def add_article(request: WSGIRequest, pk_of_scientific_publication: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	current_scientific_publication = scientific_publication.get_scientific_publication_by_id(pk_of_scientific_publication)
	volumes = volume.get_all_volumes_in_current_scientific_publication(current_scientific_publication)
	categories = category.get_all_categories_in_current_scientific_publication(current_scientific_publication)

	if request.method == "POST":
		filled_article_creation_form = ArticleForm(volumes, categories, request.POST, request.FILES)
		if filled_article_creation_form.is_valid():

			selected_volume_id = filled_article_creation_form.cleaned_data["volumes"]
			selected_category_id = filled_article_creation_form.cleaned_data["categories"]
			selected_file_name = request.FILES["file"].name

			unique_file_name = file_manager.save_file_to_server(selected_file_name, request.FILES["file"])
			russian_article = article_manager.get_name_description_and_authors_of_article_in_russian_from_file(unique_file_name)
			english_article = article_manager.get_name_description_and_authors_of_article_in_english_from_file(unique_file_name)

			volume_by_id = volume.get_volume_by_id(selected_volume_id)
			category_by_id = category.get_category_by_id(selected_category_id)

			new_article = article.add_new_article(name=russian_article["name"], short_description=russian_article["short_description"], file_name=unique_file_name,
			   authors=russian_article["authors"], user=request.user, volume=volume_by_id, category=category_by_id, decision="rejected")
			article.add_foreign_language_to_article_by_id(id=new_article.pk, name=english_article["name"], short_description=english_article["short_description"],
						 authors=english_article["authors"])
			
			return redirect("specific_user_articles_with_pagination", number_of_page=1)
		else:
			messages.error(request, "Form is invalid! Read hints")
	article_creation_form = ArticleForm(volumes, categories)
	return render(request, "article/adding_new_article.html", {"article_creation_form": article_creation_form})


@login_required
def update_article(request: WSGIRequest, pk_of_article: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	current_article = article.get_article_by_id_and_user(pk_of_article, request.user)

	if current_article is None:
		return HttpResponse("There is no article with such id")
	
	current_scientific_publication = scientific_publication.get_scientific_publication_by_id(current_article.category.scientific_publication.pk)
	volumes = volume.get_all_volumes_in_current_scientific_publication(current_scientific_publication)
	categories = category.get_all_categories_in_current_scientific_publication(current_scientific_publication)

	if request.method == "POST":
		filled_article_updating_form = ArticleForm(volumes, categories, request.POST, request.FILES)
		if filled_article_updating_form.is_valid():

			selected_volume_id = filled_article_updating_form.cleaned_data["volumes"]
			selected_category_id = filled_article_updating_form.cleaned_data["categories"]
			selected_file_name = request.FILES["file"].name

			unique_file_name = file_manager.save_file_to_server(selected_file_name, request.FILES["file"])
			file_manager.remove_file_from_server_by_name(current_article.file_name)
			russian_article = article_manager.get_name_description_and_authors_of_article_in_russian_from_file(unique_file_name)
			english_article = article_manager.get_name_description_and_authors_of_article_in_english_from_file(unique_file_name)

			volume_by_id = volume.get_volume_by_id(selected_volume_id)
			category_by_id = category.get_category_by_id(selected_category_id)

			article.update_article_by_id(id=pk_of_article, name=russian_article["name"], short_description=russian_article["short_description"],
				file_name=unique_file_name, authors=russian_article["authors"], volume=volume_by_id, category=category_by_id)
			article.add_foreign_language_to_article_by_id(id=pk_of_article, name=english_article["name"], short_description=english_article["short_description"],
						 authors=english_article["authors"])
			
			return redirect("specific_user_articles_with_pagination", number_of_page=1)
	article_updating_form = ArticleForm(volumes, categories, initial={"volumes": current_article.volume.pk, "categories": current_article.category.pk})
	return render(request, "article/updating_article.html", {"article_updating_form": article_updating_form})


@login_required
def display_remove_article_page(request: WSGIRequest, pk_of_article: int) -> HttpResponse:
	if article.get_article_by_id_and_user(pk_of_article, request.user) is None:
		return HttpResponse("There is no article with such id")
	return render(request, "article/removing_article.html", {"pk_of_article": pk_of_article})


@login_required
def remove_article(request: WSGIRequest, pk_of_article: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if article.get_article_by_id_and_user(pk_of_article, request.user) is None:
		return HttpResponse("There is no article with such id")
	
	file_manager.remove_file_from_server_by_name(article.get_article_by_id(pk_of_article).file_name)
	article.remove_article_by_id(pk_of_article)
	return redirect("specific_user_articles_with_pagination", number_of_page=1)


def display_article_with_feedbacks(request: WSGIRequest, pk_of_article: int) -> HttpResponse:
	current_article = article.get_article_by_id(pk_of_article)

	if current_article.decision != "accepted" and request.user.is_authenticated == False:
		return HttpResponse("There is no article with such id")
	
	user_middle_name = user_additional_data.get_middle_name_for_user(current_article.user)
	feedbacks_to_current_article = feedback.get_all_feedbacks_to_article(current_article)
	return render(request, "article/article_details.html", {"current_article": current_article, "feedbacks_to_current_article": feedbacks_to_current_article, "user_middle_name": user_middle_name})


def download_article(request: WSGIRequest, pk_of_article: int) -> FileResponse:
	current_article = article.get_article_by_id(pk_of_article)
	path_to_file = settings.MEDIA_ROOT + current_article.file_name
	return FileResponse(open(path_to_file, "rb"))


@login_required
@user_passes_test(user.is_user_reviewer)
def display_page_with_feedbacks_for_specific_user(request: WSGIRequest, number_of_page: int) -> HttpResponse:
	pagination_for_feedbacks = feedback.get_pagination_for_list_of_feedbacks(list_of_feedbacks=feedback.get_all_feedbacks_for_user(request.user), number_of_feedbacks_per_page=5, number_of_page_to_display=number_of_page)
	return render(request, "feedback/feedbacks_for_specific_user.html", {"pagination_for_feedbacks": pagination_for_feedbacks})


@login_required
@user_passes_test(user.is_user_reviewer)
def add_feedback(request: WSGIRequest, pk_of_article: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if request.method == "POST":
		filled_feedback_creation_form = FeedbackForm(feedback.get_decisions(), request.POST)
		if filled_feedback_creation_form.is_valid():

			comment = filled_feedback_creation_form.cleaned_data["comment"]
			decision = filled_feedback_creation_form.cleaned_data["decision"]
			current_article = article.get_article_by_id(pk_of_article)

			feedback.add_new_feedback(comment, current_article, request.user, decision)
			send_notification_email_to_user.delay(current_article.user.pk, request.user.pk, pk_of_article)
			return redirect("specific_user_feedbacks_with_pagination", number_of_page=1)
		else:
			messages.error(request, "Form is invalid! Read hints")
	feedback_creation_form = FeedbackForm(feedback.get_decisions())
	return render(request, "feedback/adding_new_feedback.html", {"feedback_creation_form": feedback_creation_form})


@login_required
@user_passes_test(user.is_user_reviewer)
def update_feedback(request: WSGIRequest, pk_of_feedback: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	current_feedback = feedback.get_feedback_by_id_and_user(pk_of_feedback, request.user)

	if current_feedback is None:
		return HttpResponse("There is no feedback with such id")
	
	if request.method == "POST":
		filled_feedback_updating_form = FeedbackForm(feedback.get_decisions(), request.POST)
		if filled_feedback_updating_form.is_valid():

			comment = filled_feedback_updating_form.cleaned_data["comment"]
			decision = filled_feedback_updating_form.cleaned_data["decision"]
			
			feedback.update_feedback_by_id(id=pk_of_feedback, comment=comment, decision=decision)
			return redirect("specific_user_feedbacks_with_pagination", number_of_page=1)
	feedback_updating_form = FeedbackForm(feedback.get_decisions(), initial={"comment": current_feedback.comment, "decision": current_feedback.decision})
	return render(request, "feedback/updating_feedback.html", {"feedback_updating_form": feedback_updating_form})


@login_required
@user_passes_test(user.is_user_reviewer)
def display_remove_feedback_page(request: WSGIRequest, pk_of_feedback: int) -> HttpResponse:
	if feedback.get_feedback_by_id_and_user(pk_of_feedback, request.user) is None:
		return HttpResponse("There is no feedback with such id")
	return render(request, "feedback/removing_feedback.html", {"pk_of_feedback": pk_of_feedback})


@login_required
@user_passes_test(user.is_user_reviewer)
def remove_feedback(request: WSGIRequest, pk_of_feedback: int) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if feedback.get_feedback_by_id_and_user(pk_of_feedback, request.user) is None:
		return HttpResponse("There is no feedback with such id")
	
	feedback.remove_feedback_by_id(pk_of_feedback)
	return redirect("specific_user_feedbacks_with_pagination", number_of_page=1)


@login_required
def change_user_additional_data(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if request.method == "POST":
		filled_user_additional_data_form = UserAdditionalDataForm(request.POST)
		if filled_user_additional_data_form.is_valid():
			user_additional_data.save_middle_name_for_user(user=request.user, new_middle_name=filled_user_additional_data_form.cleaned_data["middle_name"])
			return redirect("homepage")
		else:
			messages.error(request, "Form is invalid!")
	user_additional_data_form = UserAdditionalDataForm(instance=user_additional_data.get_object_by_user(user=request.user))
	return render(request, "user/account_settings.html", {"user_additional_data_form": user_additional_data_form})


def activate_user_account(request: WSGIRequest, code: str) -> HttpResponse:
	try:
		user_additional_data_by_code = user_additional_data.get_object_by_code(code=code)
		registered_user = User.objects.get(pk=user_additional_data_by_code.user.pk)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		registered_user = None

	if registered_user is not None:
		registered_user.is_active = True
		registered_user.save()
		return HttpResponse("Thank you for your account activation. Now you can <a href='/authorization'>login</a>.")
	else:
		return HttpResponse("Activation link is invalid!")


@login_required
def change_user_password(request: WSGIRequest) -> HttpResponse:
	if request.method == "POST":
		filled_password_change_form = PasswordChangeForm(request.user, request.POST)
		if filled_password_change_form.is_valid():
			user_with_new_password = filled_password_change_form.save()
			update_session_auth_hash(request, user_with_new_password)
			return HttpResponse("Your password successfully changed. <a href='/'>Go home</a>")
		else:
			messages.error(request, "Please make sure that you entered correct password while confirmation and old password is correct too.")
	password_change_form = PasswordChangeForm(request.user)
	return render(request, "user/change_password.html", {"password_change_form": password_change_form})


def register_new_user(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if request.user.is_authenticated:
		return redirect("homepage")
	if request.method == "POST":
		filled_registration_form = UserRegistrationForm(request.POST)
		if filled_registration_form.is_valid():

			new_user = filled_registration_form.save()
			new_user_additional_data = user_additional_data.add_new(new_user)

			send_email_message_to_user_with_activation_link.delay(new_user.pk, new_user_additional_data.code)
			return HttpResponse("We sent email with instructions to activate your account. <a href='/'>Go home</a>")
		else:
			messages.error(request, "Unsuccessful registration. Please read all hints under input fields. Hint: maybe username you entered is already in use!")
	registration_form = UserRegistrationForm()
	return render(request=request, template_name="authentication/registration.html", context={"registration_form": registration_form})


def authorize_user(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if request.user.is_authenticated:
		return redirect("homepage")
	
	if request.method == "POST":
		form_with_credentials = AuthenticationForm(request, data=request.POST)
		if form_with_credentials.is_valid():

			username = form_with_credentials.cleaned_data.get("username")
			password = form_with_credentials.cleaned_data.get("password")
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
def logout_user(request: WSGIRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
	logout(request)
	return redirect("homepage")


def reset_password(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
	if request.user.is_authenticated:
		return redirect("homepage")
	
	if request.method == "POST":
		filled_password_reset_form = PasswordResetForm(request.POST)
		if filled_password_reset_form.is_valid():

			user_email = filled_password_reset_form.cleaned_data["email"]
			associated_users = User.objects.filter(Q(email=user_email))
			
			if associated_users.exists():
				for user in associated_users:
					send_email_message_to_user_with_password_reset_link.delay(user.pk)
					return redirect ("/password_reset/done/")
		messages.error(request, "An invalid email has been entered.")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form": password_reset_form})