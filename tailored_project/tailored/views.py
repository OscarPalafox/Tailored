from django.http import HttpResponseRedirect
from django.shortcuts import render
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import Search_bar, ItemForm, CategoryForm, SectionForm, UserProfileForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
			return HttpResponseRedirect(reverse('tailored:index'))

		else:
			print(form.errors)

	return render(request, 'tailored/add_category.html', {'form': form})


"""def leave_review(request):
	"""


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

def add_item(request):
	form = ItemForm()

	if (request.method == "POST"):
		
		if (form.is_valid()):
			form.save(commit = True)
			
			return show_section(request, str(form.cleaned_data.get("section")))

		else:
			print(form.errors)

	return render(request, "tailored/add_item.html", {"form": form})

def search_bar(request,search=None,category=None):

	context_dict={}
	categories=Category.objects.all()
	
	context_dict['categories']=categories
	if(request.method=='POST'):
		check=request.POST.get('search')
		if check!=None:
			search=check
		check=request.POST.get('choose')
		if check!=None: 
			category=check
		if search != None:
			search=search.split(" ")
			searchS="_".join(search)
		items= []

		if category != None and search!=None:
			for word in search:
				
				items+=Item.objects.filter((Q(description__contains=word )|Q (title__contains=word)&(Q(category=category )|Q (category=category))))
			context_dict['category']=category
			context_dict['search']=searchS
		elif search != None:	
			for word in search:
				items+=Item.objects.filter(Q(description__contains=word )|Q (title__contains=word))
			context_dict['search']= searchS

		elif category!=None:
				
				items=Item.objects.filter(Q(category=category)|Q(category=category))
				context_dict['category']=category

		else:
			return home_page(request)
		
		context_dict['items']=items
	
		return render(request, 'tailored/search.html',context_dict)
	else :
		render(request, 'tailored/index.html')


def home_page(request):
	context_dict={}
	categories=Category.objects.all()
	
	context_dict['categories']=categories

	#placeholder for homepage, feel free to change it.

	return render(request, 'tailored/index.html', context_dict)