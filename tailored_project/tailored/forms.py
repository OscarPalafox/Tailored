
from django import forms
from tailored.models import Item, Category, Section, Size
from datetime import date
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

	itemPic = forms.ImageField(required = False, 
		help_text = "Upload a picture of the item: ")
	
	description = forms.CharField(widget=forms.Textarea, 
		help_text = "Please give a brief description of the item.")
	datePosted = forms.DateField(widget=forms.HiddenInput(), initial = date.today)
	
	dailyVisits = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

	
	size = forms.ModelChoiceField(queryset = Size.objects.all(), help_text = "Select the size: ")
	
	class Meta:
		model = Item
		exclude = ("itemID", "sold", )
		

