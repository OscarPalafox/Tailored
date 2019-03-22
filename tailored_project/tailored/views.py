from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import Search_bar, ItemForm, EditUserProfileForm, UserProfileForm, ReviewForm, EditItemForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.contrib.auth.models import User
from django import forms


def show_item(request, itemID):
	item = get_object_or_404(Item, itemID = itemID)
	print(item)
	context_dict = {}
	context_dict['item'] = item
	
	print(item.dailyVisits, 'before')
	related=Item.objects.filter(category=item.category)
	context_dict['trendingItems']=related
	response=render(request, 'tailored/product.html', context_dict)
	if first_visit(request, response, str(item.itemID)):
		print('HEY')
		item.dailyVisits += 1
		item.save()


	print(item.dailyVisits, 'after')

	return response


def get_trending_items():
	items = Item.objects.all()
	trending = []

	for item in Item.objects.order_by('-dailyVisits'):
		if ( ((date.today() - item.datePosted).days <= 0) and (item.sold_to == None)):
			if (len(trending) <= 5):
				trending.append(item)
		else:
			item.dailyVisits = 0
			item.save()
	for item in Item.objects.order_by('-dailyVisits'):
		if ((len(trending)) <= 5 and (item.sold_to == None) and (item not in trending)):
			trending.append(item)
	
	return trending


def trending(request):
	items = Item.objects.all()
	trending = []

	for item in Item.objects.order_by('-dailyVisits'):
		if ( ((date.today() - item.datePosted).days <= 0) and (item.sold_to == None)):
			if (len(trending) <= 5):
				trending.append(item)
		else:
			item.dailyVisits = 0
			item.save()

	if (len(trending) <= 5):
		for item in Item.objects.order_by('-dailyVisits'):
			if ((len(trending) <= 5) and (item.sold_to == None) and (item not in trending)):
				trending.append(item)
	

	context_dict = {"trendingItems": trending}
	return render(request, 'tailored/index.html', context_dict)


def items(request):
	item_list = Item.objects.order_by('-dailyVisits')[:5]
	context_dict = {'items': item_list}

	return render(request, 'tailored/itemsList.html', context_dict)


def show_section(request, title):
	context_dict = {}

	try:
		title = title.lower().capitalize()
		
		section = Section.objects.get(title = title)
		items = Item.objects.filter(section = section)
		context_dict['items'] = items
		context_dict['section'] = section

	except Section.DoesNotExist:

		context_dict['section'] = None
		context_dict['items'] = None

	return render(request, 'tailored/section.html', context_dict)


def show_category(request, title):
	context_dict = {}

	try:
		title = title.lower()
		
		category = Category.objects.get(slug = title)
		items = Item.objects.filter(category = category)
		context_dict['items'] = items
		context_dict['category'] = category

	except Category.DoesNotExist:

		context_dict['category'] = None
		context_dict['items'] = None

	return render(request, 'tailored/category.html', context_dict)


@login_required
def user_profile(request):
	form = ItemForm()

	user_profile = get_object_or_404(UserProfile, user = User.objects.get(username = request.user))
	context_dict = {}
	context_dict["user_profile"] = user_profile
	context_dict['user_rating'] = range(round(user_profile.rating, 1))
	
	reviews_user = Review.objects.filter(Q(item__in = Item.objects.filter(seller = user_profile)))
	
	context_dict['reviews_user'] = reviews_user.order_by('-datePosted')

	user_items = Item.objects.filter(seller = user_profile)
	context_dict['user_items'] = user_items

	if (request.method == "POST"):
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			item = form.save(commit = False)
			item.seller = UserProfile.objects.get(user = request.user)
			item.save()
			return HttpResponseRedirect(reverse('tailored:index'))
		else:
			print(form.errors)
	context_dict["form"] = form
	return render(request, "tailored/user_profile.html", context_dict)


def show_seller_profile(request, seller_username):
	context_dict = {}
	
	seller_user = get_object_or_404(User, username = seller_username)
	context_dict['seller_user'] = seller_user
	
	seller_user_profile = get_object_or_404(UserProfile, user = seller_user)
	context_dict['seller_user_profile'] = seller_user_profile
	context_dict['seller_rating'] = range(int(round(seller_user_profile.rating, 1)))

	seller_items = Item.objects.filter(seller = seller_user_profile)
	itemList = []

	for item in seller_items:
		if (item.sold_to == None):
			itemList.append(item)

	context_dict['seller_items'] = itemList

	reviews_seller = Review.objects.filter(Q(item__in = Item.objects.filter(seller = seller_user_profile)))
	
	context_dict['reviews_seller'] = reviews_seller.order_by('-datePosted')

	if request.user.is_authenticated():
		items_reviewed = []
		for review in Review.objects.select_related():
			items_reviewed.append(review.item.itemID)
		
		items_to_review = Item.objects.filter(Q(sold_to__in = UserProfile.objects.filter( 
													user__in = User.objects.filter(username = request.user))) &
									Q(seller = seller_user_profile)
									).exclude(itemID__in = items_reviewed)
		
		context_dict['items_to_review'] = items_to_review

		if items_to_review:
			form = ReviewForm(user_items = items_to_review)
			if(request.method == 'POST'):
				form = ReviewForm(items_to_review, request.POST)
				if form.is_valid():
					review = form.save()
					# Remove item just reviewed from the items to review
					context_dict['items_to_review'] = items_to_review.exclude(itemID = review.item.itemID)

					# Handle if there are more items to review
					if context_dict['items_to_review']:
						context_dict['form'] = ReviewForm(user_items = context_dict['items_to_review'])

					reviews_seller_updated = Review.objects.filter(Q(item__in = Item.objects.filter(
																		seller = seller_user_profile)))
					rating = 0
					for review_updated in list(reviews_seller_updated):
						rating += review_updated.rating
					rating = round(rating/len(reviews_seller_updated), 1)

					seller_user_profile.rating = rating
					seller_user_profile.save()

					return HttpResponseRedirect(reverse('tailored:show_seller_profile',
							kwargs = {'seller_username': seller_username}))

			context_dict['form'] = form
	return render(request, 'tailored/seller_profile.html', context_dict)


@login_required
def user_profile(request):
	user = User.objects.get(username = request.user)
	user_profile = get_object_or_404(UserProfile, user = user)

	context_dict = {}
	context_dict["user_profile"] = user_profile
	context_dict['user_rating'] = range(int(round(user_profile.rating, 0)))
	
	reviews_user = Review.objects.filter(Q(item__in = Item.objects.filter(seller = user_profile)))
	context_dict['reviews_user'] = reviews_user.order_by('-datePosted')

	item_form = ItemForm()
	user_form = EditUserProfileForm()

	if (request.method == "POST"):
		item_form = ItemForm(request.POST, request.FILES)
		user_form = EditUserProfileForm(request.POST, request.FILES)
		
		if item_form.is_valid():
			item = item_form.save(commit = False)
			item.seller = user_profile
			item.save()

			context_dict['user_form'] = user_form
			return HttpResponseRedirect(reverse('tailored:index'))

		elif user_form.is_valid():
			if user_form.has_changed():
				user_form_keys = list(user_form.cleaned_data.keys())
				
				for key in user_form_keys[:2]:
					if user_form.cleaned_data[key] and user.__dict__[key] != user_form.cleaned_data[key]:
						user.__dict__[key] = user_form.cleaned_data[key]
				user.save()

				for key in user_form_keys[2:]:
					if user_form.cleaned_data[key] and profile_user.__dict__[key] != user_form.cleaned_data[key]:
						profile_user.__dict__[key] = user_form.cleaned_data[key]
				user_profile.save()
				context_dict["item_form"] = item_form
				return HttpResponseRedirect(reverse('tailored:index'))
			else:
				keys = list(user_form.cleaned_data.keys())
				for key in keys:
					user_form.add_error(key, forms.ValidationError("You need to fill at least one field."))
				context_dict["item_form"] = item_form
				context_dict['user_form'] = user_form
				return render(request, 'tailored/user_profile.html', context_dict)

	context_dict["item_form"] = item_form
	context_dict['user_form'] = user_form
	return render(request, "tailored/user_profile.html", context_dict)


@login_required
def edit_item(request, itemID):
	context_dict = {}
	item = get_object_or_404(Item, itemID = itemID)
	
	if (item.seller.user != request.user):
		raise Http404

	form = EditItemForm()
	context_dict['itemID'] = item.itemID
	
	if request.method == 'POST':
		form = EditItemForm(request.POST or None, request.FILES)
		print(form)
		if form.is_valid():
			form_keys = form.cleaned_data.keys()
			for key in form_keys:
				if key == 'sold_to':
					if form.cleaned_data['sold_to']:
						user_query = User.objects.filter(username = form.cleaned_data['sold_to'])
						
						if not user_query:
							form.add_error('sold_to', forms.ValidationError('The given user does not exist.'))
							context_dict['form'] = form
							return render(request, 'tailored/edit_item.html', context_dict)

						elif user_query[0] != request.user:
							try:
								print(user_query[0])
								item.sold_to = UserProfile.objects.get(user = user_query[0])
								item.save()
							except UserProfile.DoesNotExist:
								form.add_error('sold_to', forms.ValidationError('The given user does not exist.'))
								context_dict['form'] = form
								return render(request, 'tailored/edit_item.html', context_dict)
						else:
							form.add_error('sold_to', forms.ValidationError("You can't sell an item to yourself."))
							context_dict['form'] = form
							return render(request, 'tailored/edit_item.html', context_dict)

			return HttpResponseRedirect(reverse('tailored:index'))

	context_dict['form'] = form
	return render(request, 'tailored/edit_item.html', context_dict)


def search_bar(request, search = None, page=1):	
	categories = Category.objects.all()
	
	
	if(request.method == 'POST'):
		check = request.POST.get('search')
		print(check, "CHECK")
		if check != None:
			if check != "":
				return HttpResponseRedirect(check + "/")
			else:
				return HttpResponseRedirect(reverse('tailored:search', kwargs = {'search': 'all'}))
		else:
			return HttpResponseRedirect('all/')

	context_dict = {}
	context_dict['categories'] = categories
	items = []	
	if search == "all" or search == None or search == "":
		search = "all"
		items = Item.objects.all()
	else:
		if search != None:
			search = search.split(" ")
			for word in search:
				items += Item.objects.filter(Q(description__contains = word ) | Q(title__contains = word)
					| Q(category = word) | Q(section = word))
			searchS = "_".join(search)
			context_dict['search'] = searchS
		else:
			return home_page(request)
	maxi = 0
	for item in items:
		if item.price > maxi:
			maxi = item.price
	context_dict['maxi'] = maxi
	context_dict['page']  = page
	context_dict['items'] = items
	context_dict['pages']= int(len(items)/6)
	context_dict['min'] = 6 * (int(page) - 1)
	context_dict['max'] = 6 * (int(page))
	return render(request, 'tailored/shop_bootstrap.html',context_dict)


def new_in(request, search = None, page = 1):
	context_dict = {}
	items = []	
	search = search
	print("hello")
	if search != None:
		search = search.split(" ")
		toAdd = []
		for word in search:

			toAdd += Item.objects.filter(Q(description__contains = word ) | Q(title__contains = word)
				| Q(category = word) | Q(section = word))
			for item in toAdd:
				if (date.today()- item.datePosted).days<=7:
					items+=[item]
		searchS="_".join(search)
		maxi = 0
		for item in items:
			if item.price > maxi:
				maxi = item.price
		context_dict['maxi'] = maxi + 5
		context_dict['search'] = searchS
		context_dict['page']  = page
		context_dict['items'] = items
		context_dict['pages'] = int(len(items)/6)
		context_dict['min'] = 6 * (int(page) - 1)
		context_dict['max'] = 6 * (int(page))
		return render(request, 'tailored/shop_bootstrap.html',context_dict)
	else:
		return home_page(request)


def home_page(request):
	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories

	#placeholder for homepage, feel free to change it.
	return render(request, 'tailored/index.html', context_dict)

def first_visit(request, response, item):
	
	last_visit_cookie = request.COOKIES.get('last_visit' + item, "first")
	
	if(last_visit_cookie == "first"):
		response.set_cookie('last_visit' + item, str(datetime.now()))
		return True
	else:
		last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
		if ((datetime.now() - last_visit_time).days > 0):
			response.set_cookie('last_visit' + item, str(datetime.now()))
			return True
		else:
			response.set_cookie('last_visit' + item , last_visit_cookie)
			return False