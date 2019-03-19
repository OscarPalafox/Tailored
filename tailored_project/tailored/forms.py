from django import forms
from tailored.models import Item, Category, Section, UserProfile, Review, Size
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
	def __init__(self, section_set, *args, **kwargs):
		super(ItemForm, self).__init__(*args, **kwargs)
		self.fields['section'] = forms.ModelChoiceField(queryset = section_set, help_text = "Select a section: ")

	title = forms.CharField(max_length = 128,
		help_text = "Please enter the name of the item: ")
	
	price = forms.DecimalField(help_text = "Enter the price: ", min_value = 0, decimal_places = 2)

	#section = forms.ModelChoiceField(queryset = Section.objects.all(), help_text = "Select a section: ")
	category = forms.ModelChoiceField(queryset = Category.objects.all(), help_text = "Select a category: ")

	picture = forms.ImageField(required = False, 
		help_text = "Upload a picture of the item: ")
	
	description = forms.CharField(widget = forms.Textarea, 
		help_text = "Please give a brief description of the item.")
	datePosted = forms.DateField(widget = forms.HiddenInput(), initial = date.today)
	
	dailyVisits = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

	
	size = forms.ModelChoiceField(queryset = Size.objects.all(), help_text = "Select the size: ")
	
	class Meta:
		model = Item
		exclude = ("itemID", "sold_to", "sellerID")

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


class ReviewForm(forms.ModelForm):
	#reviewID = models.IntegerField(primary_key = True)
	#buyerID = models.ForeignKey(UserProfile)
	#itemID = models.ForeignKey(Item)
	rating = forms.IntegerField(min_value = 0, max_value = 5)
	review_text = forms.CharField(widget = forms.Textarea, 
		help_text = "Please give a brief review of the seller.", required = False)
	datePosted = forms.DateField(widget = forms.HiddenInput(), initial = date.today)


	def __init__(self, user_items, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		self.fields['item'] = forms.ModelChoiceField(queryset = user_items, help_text = "Select an item: ")

	class Meta:
		model = Review
		exclude = ("reviewID", "buyer")
		#fields = ('rating', 'review_text', 'datePosted')