
from django import forms
from tailored.models import Item
class Search_bar(forms.ModelForm):
	search = forms.CharField()
	class Meta:
		model=Item
		fields = ('search',)