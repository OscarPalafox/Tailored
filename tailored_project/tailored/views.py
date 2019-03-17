from django.shortcuts import render
from tailored.models import Item, Category
from tailored.forms import Search_bar
from django.db.models import Q
# Create your views here.

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
