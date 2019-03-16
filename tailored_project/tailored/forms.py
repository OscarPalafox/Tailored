from django import forms
from django.contrib.auth.models import User
from tailored.models import Section, Category, Item, UserProfile, Review

class CategoryForm(forms.ModelForm):
	title = forms.CharField(max_length = 128, help_text = "Please enter the category title:")

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = Category
		fields = ('title',)


class SectionForm(forms.ModelForm):
	title = forms.CharField(max_length = 128, help_text = "Please enter the section title:")

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = Section
		fields = ('title',)


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture', 'postcode', 'phone')