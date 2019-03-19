from django import forms
from tailored.models import Item, Category, Section, Size, UserProfile, Review
from datetime import date
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

class Search_bar(forms.ModelForm):
	search = forms.CharField()
	class Meta:
		model=Item
		fields = ('search',)

class ItemForm(forms.ModelForm):
	title = forms.CharField(max_length = 128,
		help_text = "Please enter the name of the item: ")
	
	price = forms.IntegerField(help_text = "Enter the price: ")
	
	section = forms.ModelChoiceField(queryset = Section.objects.all(), help_text = "Select a section: ")
	category = forms.ModelChoiceField(queryset = Category.objects.all(), help_text = "Select a category: ")
	
	description = forms.CharField(widget=forms.Textarea, 
		help_text = "Please give a brief description of the item.")
	datePosted = forms.DateField(widget=forms.HiddenInput(), initial = date.today)
	
	dailyVisits = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

	size = forms.ModelChoiceField(queryset = Size.objects.all(), help_text = "Select the size: ")
        itemPic = forms.ImageField(required = False, 
		help_text = "Upload a picture of the item: ")	
	class Meta:
		model = Item
		exclude = ("itemID", "sold", )

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


class UserProfileForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
	first_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	last_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	picture = forms.ImageField(required = False)
	postcode = forms.CharField(max_length = 8, validators = [RegexValidator(r'^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$')])
	phone = forms.CharField(max_length = 8, validators = [RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]*$')], required = False)
        field_order = ['first_name', 'last_name','postcode','picture','phone']

"""class ReviewForm(forms.ModelForm):
	"""
