from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import CategoryForm, SectionForm, UserForm, UserProfileForm

def index(request):
	return render(request, 'tailored/index.html')


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
			return HttpResponseRedirect(reverse('tailored:items'))

		else:
			print(form.errors)

	return render(request, 'tailored/add_category.html', {'form': form})


def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		user_profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and user_profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = user_profile_form.save(commit = False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()

			registered = True

		else:
			print(user_form.errors, user_profile_form.errors)

	else:
		user_form = UserForm()
		user_profile_form = UserProfileForm()

	return render(request, 'tailored/register.html', {'user_form': user_form, 'user_profile_form': user_profile_form,
													'registered': registered})