from django.http import HttpResponseRedirect
from django.shortcuts import render
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import Search_bar, ItemForm, CategoryForm, SectionForm, UserProfileForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import CategoryForm, SectionForm, UserProfileForm, Search_bar
from datetime import datetime
def show_item(request, itemID):
	item= Item.objects.filter(itemID=itemID)
	context_dict={}
	context_dict['items']=item
	if first_visit(request):
		print("increase daily views ")
	return render(request, 'tailored/product.html', context_dict)

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
		form = ItemForm(request.POST)
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
	
		return render(request, 'tailored/shop_bootstrap.html',context_dict)
	else :
		render(request, 'tailored/index.html', context_dict)


def home_page(request):
	context_dict={}
	categories=Category.objects.all()
	
	context_dict['categories']=categories

	#placeholder for homepage, feel free to change it.



	return render(request, 'tailored/index.html', context_dict)


def first_visit(request):
	first= get_server_side_cookie(request,'last_visit')==None
	last_visit_cookie = get_server_side_cookie(request,
												'last_visit',
													str(datetime.now()))

	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
											'%Y-%m-%d %H:%M:%S')
	if ((datetime.now() - last_visit_time).days > 0) or first:
		request.session['last_visit'] = str(datetime.now())

		return True
	else:
		print (last_visit_time)
		request.session['last_visit'] = last_visit_cookie
		return False

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

