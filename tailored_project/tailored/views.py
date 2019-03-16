from django.shortcuts import render
from tailored.models import Item
from tailored.forms import Search_bar
from django.db.models import Q
# Create your views here.

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