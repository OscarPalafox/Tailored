from django.shortcuts import render
from django.db.model import Q
# Create your views here.

def search_bar(request):
	search_bar=Search_bar()
	if(request.method=='POST'):
		search_bar=Search_bar(request.POST)
		query=request.POST.get('search')
		items= []
		for word in query:
				items+=Item.objects.filter(Q(itemName__icontains=word))
		return render(items, 'search.html')

