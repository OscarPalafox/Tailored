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
	context_dict = {}
	context_dict['items'] = item
	print(item.dailyVisits, 'before')
	
	if first_visit(request):
		item.dailyVisits += 1
		item.save()
		print('increase daily views ')
	
	print(item.dailyVisits, 'after')
	return render(request, 'tailored/product.html', context_dict)

def trending(request):
	items = Item.objects.all()
	trending = []

	for item in Item.objects.order_by('-dailyVisits'):
		
		if ( (date.today() - item.datePosted).days <= 0 ):
			if (len(trending) < 5):
				trending.append(item)
		else:
			item.dailyVisits = 0
			item.save()

	context_dict = {'trendingItems': trending}
	return render(request, 'tailored/trending.html', context_dict)


def index(request):
	return render(request, 'tailored/index.html')


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
def add_item(request):
	form = ItemForm()
	seller = get_object_or_404(UserProfile, user = request.user)

	if request.method == 'POST':
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			item = form.save(commit = False)
			item.seller = seller
			item.save()
			return HttpResponseRedirect(reverse('tailored:show_section',
				kwargs = {'title': str(form.cleaned_data.get('section'))}))
		else:
			print(form.errors)
	return render(request, 'tailored/add_item.html', {'form': form})


def show_seller_profile(request, seller_username):
	context_dict = {}
	
	seller_user = get_object_or_404(User, username = seller_username)
	context_dict['seller_user'] = seller_user
	
	seller_user_profile = get_object_or_404(UserProfile, user = seller_user)
	context_dict['seller_user_profile'] = seller_user_profile

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
	return render(request, 'tailored/Sprofile.html', context_dict)


@login_required
def edit_profile(request):
	user = User.objects.get(username = request.user)
	profile_user = get_object_or_404(UserProfile, user = request.user)
	form = EditUserProfileForm()

	if request.method == 'POST':
		form = EditUserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			if form.has_changed():
				form_keys = list(form.cleaned_data.keys())
				
				for key in form_keys[:2]:
					if form.cleaned_data[key] and user.__dict__[key] != form.cleaned_data[key]:
						user.__dict__[key] = form.cleaned_data[key]
				user.save()

				for key in form_keys[2:]:
					if form.cleaned_data[key] and profile_user.__dict__[key] != form.cleaned_data[key]:
						profile_user.__dict__[key] = form.cleaned_data[key]
				profile_user.save()
				return HttpResponseRedirect(reverse('tailored:index'))
			else:
				keys = list(form.cleaned_data.keys())
				for key in keys:
					form.add_error(key, forms.ValidationError("You need to fill at least one field."))
				return render(request, 'tailored/edit_profile.html', {'form': form})

	return render(request, 'tailored/edit_profile.html', {'form': form})


@login_required
def edit_item(request, itemID):
	context_dict = {}
	item = get_object_or_404(Item, itemID = itemID)
	
	if (item.seller.user != request.user):
		raise Http404

	form = EditItemForm()
	context_dict['itemID'] = item.itemID
	
	if request.method == 'POST':
		form = EditItemForm(request.POST, request.FILES)

		if form.is_valid():
			if form.has_changed():
				form_keys = form.cleaned_data.keys()
				for key in form_keys:
					if key == 'section' or key == 'category' or key == 'size':
						if form.cleaned_data[key] and item.__dict__[key + '_id'] != form.cleaned_data[key]:
							item.__dict__[key] = form.cleaned_data[key]

					elif key == 'sold_to':
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

					else:
						if form.cleaned_data[key] and item.__dict__[key] != form.cleaned_data[key]:
							item.__dict__[key] = form.cleaned_data[key]
							item.__dict__[key] = form.cleaned_data[key]
				item.save()
				return HttpResponseRedirect(reverse('tailored:index'))

			else:
				keys = list(form.cleaned_data.keys())
				for key in keys:
					form.add_error(key, forms.ValidationError("You need to fill at least one field."))
				context_dict['form'] = form
				return render(request, 'tailored/edit_item.html', context_dict)

	context_dict['form'] = form
	return render(request, 'tailored/edit_item.html', context_dict)


def search_bar(request, search = None, category = None):

	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories
	if(request.method == 'POST'):
		check = request.POST.get('search')
		if check != None:
			search = check
		check = request.POST.get('choose')
		if check != None: 
			category = check
		if search != None:
			search = search.split(' ')
			searchS = '_'.join(search)
		items = []

		if category != None and search != None:
			for word in search:
				items += Item.objects.filter((Q(description__contains = word) | Q(title__contains = word) & (Q(category = category) | Q(category = category))))
			
			context_dict['category'] = category
			context_dict['search'] = searchS

		elif search != None:	
			for word in search:
				items += Item.objects.filter(Q(description__contains = word ) | Q(title__contains = word))
			
			context_dict['search'] = searchS

		elif category != None:
				
				items = Item.objects.filter(Q(category = category) | Q(category = category))
				context_dict['category'] = category

		else:
			return home_page(request)
		
		context_dict['items'] = items
	

		return render(request, 'tailored/shop_bootstrap.html',context_dict)

	else:
		render(request, 'tailored/index.html', context_dict)


def home_page(request):
	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories

	#placeholder for homepage, feel free to change it.
	return render(request, 'tailored/index.html', context_dict)


def first_visit(request):
	first = get_server_side_cookie(request,'last_visit') == None
	last_visit_cookie = get_server_side_cookie(request,
												'last_visit',
													str(datetime.now()))

	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
											'%Y-%m-%d %H:%M:%S')
	if ((datetime.now() - last_visit_time).days > 0) or first:
		request.session['last_visit'] = str(datetime.now())
		return True

	else:
		request.session['last_visit'] = last_visit_cookie
		return False


def get_server_side_cookie(request, cookie, default_val = None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val