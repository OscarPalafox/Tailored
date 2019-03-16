from django.shortcuts import render
from tailored.models import Item
from tailored.forms import Search_bar
from django.db.models import Q
# Create your views here.

def search_bar(request, categories=None):
	
	if(request.method=='POST'):

		query=request.POST.get('search').split(" ")
		items= []
		if categories is None:
			for word in query:
				items+=Item.objects.filter(Q(description__contains=word )|Q (title__contains=word))

		else:
			for word in query:
					
				items+=Item.objects.filter((Q(description__contains=word )|Q (title__contains=word)& Q(categories__contains=category)))


		context_dict={}
		context_dict['items']=items
		return render(request, 'tailored/search.html',context_dict)

def home_page(request):
	
	#placeholder for homepage, feel free to change it.


	return render(request, 'tailored/index.html')
def categories(request):
	if(request.method=='POST'):
		categories=request.POST.get('categories')
		context_dict={}
		context_dict['categories':categories]
		return render(request,'tailored/index.html', categories)

