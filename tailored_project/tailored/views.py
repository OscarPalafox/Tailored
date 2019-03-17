from django.shortcuts import render
from tailored.models import Section, Item, Category
from tailored.forms import Search_bar
from django.db.models import Q

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
		return render(request, 'tailored/search.html',context_dict)

def home_page(request):
	
	#placeholder for homepage, feel free to change it.
	
	return render(request, 'tailored/index.html')
