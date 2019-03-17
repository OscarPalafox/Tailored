from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
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


class UserProfileForm(RegistrationForm):
	first_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	last_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	picture = forms.ImageField(required = False)
	postcode = forms.CharField(max_length = 8)
	phone = forms.CharField(max_length = 8, validators = [RegexValidator(r'^\d{0,10}$')], required = False)

class Search_bar(forms.ModelForm):
	search = forms.CharField()
	class Meta:
		model = Item
		fields = ('search',)