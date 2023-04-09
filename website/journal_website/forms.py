from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
		if commit:
			new_user.save()
		return new_user