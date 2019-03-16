from django.shortcuts import render
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import CategoryForm, SectionForm

def items(request):
	item_list = Item.objects.order_by('-dailyVisits')[:5]
	context_dict = {'items': item_list}

	return render(request, 'tailored/itemsList.html', context_dict)

def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return index(request)

		else:
			print(form.errors)

	return render(request, 'rango:add_category', {'form': form})