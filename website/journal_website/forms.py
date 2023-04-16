from typing import Required
from django.core.validators import FileExtensionValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import UserAdditionalData, Feedback


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=70, required=True)
	last_name = forms.CharField(max_length=70, required=True)
	

	class Meta:
		model = User
		fields = ("username", "password1", "password2", "email", "first_name", "last_name")


	def save(self, commit=True):
		new_user = super(UserRegistrationForm, self).save(commit=False)
		new_user.email = self.cleaned_data['email']
		new_user.first_name = self.cleaned_data['first_name']
		new_user.last_name = self.cleaned_data['last_name']
		new_user.is_active = False
		if commit:
			new_user.save()
		return new_user


class UserAdditionalDataForm(ModelForm):
	class Meta:
		model = UserAdditionalData
		fields = ["middle_name"]


class ArticleForm(forms.Form):
	volumes = forms.ChoiceField(choices=[], required=True)
	categories = forms.ChoiceField(choices=[], required=True)
	file = forms.FileField(label='Choose DOCX or DOC file', validators=[FileExtensionValidator(allowed_extensions=["docx", "doc"])], required=True)
    

	def __init__(self, volumes_in_current_scientific_publication, categories_in_current_scientific_publication, *args, **kwargs):
		super(ArticleForm, self).__init__(*args, **kwargs)
		try:
			self.fields["volumes"].choices=[(volume.pk, volume.name) for volume in volumes_in_current_scientific_publication]
			self.fields["categories"].choices=[(category.pk, category.name) for category in categories_in_current_scientific_publication]
		except:
			raise Exception("Couldn't intialize choise fields on form")


class FeedbackForm(forms.Form):
	comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your feedback here', 'rows': 10, 'cols': 30}), required=True)
	decision = forms.ChoiceField(choices=[], required=True)


	def __init__(self, decicions, *args, **kwargs):
		super(FeedbackForm, self).__init__(*args, **kwargs)
		try:
			self.fields["decision"].choices=decicions
		except:
			raise Exception("Couldn't intialize choise field on form")