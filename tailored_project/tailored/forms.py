from django import forms
from tailored.models import Item, Category, Section, Size, UserProfile, Review
from datetime import date
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Search_bar(forms.ModelForm):
	search = forms.CharField(label="", required=False )

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = Item
		fields = ('search',)


class ItemForm(forms.ModelForm):
	title = forms.CharField(max_length = 128, help_text = 'Please enter the name of the item: ')
	price = forms.DecimalField(help_text = 'Enter the price: ', min_value = 0, decimal_places = 2)

	section = forms.ModelChoiceField(queryset = Section.objects.all(), help_text = 'Select a section: ')
	category = forms.ModelChoiceField(queryset = Category.objects.all(), help_text = 'Select a category: ')

	picture= forms.ImageField(required = False, help_text = 'Upload a picture of the item: ')
	
	description = forms.CharField(widget = forms.Textarea,
									help_text = 'Please give a brief description of the item.')
	size = forms.ModelChoiceField(queryset = Size.objects.all(), help_text = 'Select the size: ')

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = Item
		exclude = ('itemID', 'sold_to', 'seller', 'datePosted', 'dailyVisits')


class UserProfileForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
	first_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	last_name = forms.CharField(max_length = 128, validators = [RegexValidator(r'^([^0-9]*)$')])
	picture = forms.ImageField(required = False)
	postcode = forms.CharField(max_length = 8, validators = [RegexValidator(r'^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$')])
	phone = forms.CharField(max_length = 8, required = False, validators = [RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]*$')])

	# Specify the order of the fields
	field_order = ["first_name", "last_name", "phone", "postcode", "picture"]


class ReviewForm(forms.ModelForm):
	rating = forms.IntegerField(help_text = 'Rate the seller out of 5:', min_value = 0, max_value = 5)
	review_text = forms.CharField(widget = forms.Textarea, 
		help_text = 'Please give a brief review of the seller.', required = False)

	def __init__(self, user_items, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		self.fields['item'] = forms.ModelChoiceField(queryset = user_items, help_text = 'Select an item to review: ')

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = Review
		exclude = ('buyer', 'datePosted')


class EditUserProfileForm(forms.ModelForm):
	first_name = forms.CharField(help_text = 'First name: ', required = False, max_length = 128,
									validators = [RegexValidator(r'^([^0-9]*)$')])
	last_name = forms.CharField(help_text = 'Last name: ', required = False, max_length = 128,
									validators = [RegexValidator(r'^([^0-9]*)$')])
	picture = forms.ImageField(help_text = 'Picture: ', required = False)
	postcode = forms.CharField(help_text = 'Postcode: ', required = False, max_length = 8,
								validators = [RegexValidator(r'^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$')])
	phone = forms.CharField(help_text = 'Phone: ', required = False, max_length = 8,
						validators = [RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]*$')])

	# Inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model
		model = UserProfile
		fields = ('first_name', 'last_name', 'picture', 'postcode', 'phone')


class EditItemForm(forms.ModelForm):

	sold_to = forms.CharField(max_length = 128,
				help_text = 'Please enter the username of the buyer: ')

	class Meta:
		model = Item
		fields = []