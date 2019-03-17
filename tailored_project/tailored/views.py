from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import CategoryForm, SectionForm, UserProfileForm

def index(request):
	return render(request, 'tailored/index.html')


def items(request):
	item_list = Item.objects.order_by('-dailyVisits')[:5]
	context_dict = {'items': item_list}

	return render(request, 'tailored/itemsList.html', context_dict)

@login_required
def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return HttpResponseRedirect(reverse('tailored:items'))

		else:
			print(form.errors)

	return render(request, 'tailored/add_category.html', {'form': form})