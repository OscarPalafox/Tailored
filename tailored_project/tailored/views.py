from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import CategoryForm, SectionForm, UserProfileForm, Search_bar

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


def show_section(request, title):
	context_dict = {}

	try:
		title = title.lower().capitalize()
		
		section = Section.objects.get(title = title)
		items = Item.objects.filter(section = section)
		context_dict["items"] = items
		context_dict["section"] = section

	except Section.DoesNotExist:

		context_dict["section"] = None
		context_dict["items"] = None

	return render(request, "tailored/section.html", context_dict)


def show_category(request, title):
	context_dict = {}

	try:
		title = title.lower()
		
		category = Category.objects.get(slug = title)
		items = Item.objects.filter(category = category)
		context_dict["items"] = items
		context_dict["category"] = category

	except Category.DoesNotExist:

		context_dict["category"] = None
		context_dict["items"] = None

	return render(request, "tailored/category.html", context_dict)


def search_bar(request):
	
	if(request.method=='POST'):

		query=request.POST.get('search').split(" ")
		items= []
		for word in query:
			items+=Item.objects.filter(Q(description__contains=word )|Q (title__contains=word))
			print(items)
		context_dict={}
		context_dict['items']=items
		
		return render(request, 'tailored/search.html', context_dict)


def home_page(request):
	
	#placeholder for homepage, feel free to change it.
	
	return render(request, 'tailored/home.html')