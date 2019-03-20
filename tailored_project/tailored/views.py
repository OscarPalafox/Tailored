from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import Search_bar, ItemForm, UserProfileForm, ReviewForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
#from django.contrib import auth
from django.contrib.auth.models import User

def show_item(request, itemID):
	item = Item.objects.filter(itemID = itemID)
	context_dict = {}
	context_dict['items'] = item
	if first_visit(request):
		print("increase daily views ")
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

	context_dict = {"trendingItems": trending}
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

@login_required
def add_item(request):
	try:
		form = ItemForm()

		if (request.method == "POST"):
			form = ItemForm(request.POST, request.FILES)
			if form.is_valid():
				item = form.save(commit = False)
				item.seller = UserProfile.objects.get(user = request.user)
				item.save()
				return HttpResponseRedirect(reverse('tailored:show_section',
					kwargs = {'title': str(form.cleaned_data.get("section"))}))
			else:
				print(form.errors)
		return render(request, "tailored/add_item.html", {"form": form})
	except:
		return HttpResponse("You're an admin, add the item from the admin website.")


@login_required
def leave_review(request):
	return None
	items_reviewed = []

	for review in Review.objects.select_related():
		items_reviewed.append(review.item.itemID)
	
	items_to_review = Item.objects.filter(sold_to = UserProfile.objects.get(user = request.user)
								).exclude(itemID__in = items_reviewed)

	#print(not items_to_review) Empty queryset

	form = ReviewForm(user_items = items_to_review)

	if(request.method == "POST"):
		form = ReviewForm(items_to_review, request.POST)
		if form.is_valid():
			review = form.save(commit = False)
			#review.buyer = UserProfile.objects.get(user = request.user)
			review.save()

			return HttpResponseRedirect(reverse('tailored:show_seller_profile',
					kwargs = {'seller_username': request["seller"].username}))
		else:
			print(form.errors)
	return render(request, "tailored/user_profile.html", {"form": form})


def show_seller_profile(request, seller_username):
	context_dict = {}
	seller_user = get_object_or_404(User, username = seller_username)
	context_dict['seller_user'] = seller_user

	reviews_seller = Review.objects.filter(Q(item__in = Item.objects.filter(seller = UserProfile.objects.get
																						(user = seller_user))))

	print(reviews_seller)
	
	context_dict['reviews_seller'] = reviews_seller.order_by('-datePosted')

	rating = 0
	
	if reviews_seller:
		for review in list(reviews_seller):
			rating += review.rating
		rating = rating/len(reviews_seller)
	
	context_dict['seller_rating'] = rating

	if request.user.is_authenticated():
		try:
			items_reviewed = []
			for review in Review.objects.select_related():
				items_reviewed.append(review.item.itemID)
			
			items_to_review = Item.objects.filter(Q(sold_to = UserProfile.objects.get(user = request.user)) &
										Q(seller = UserProfile.objects.get(user = seller_user))
										).exclude(itemID__in = items_reviewed)
			
			context_dict['items_to_review'] = items_to_review
			if items_to_review:
				form = ReviewForm(user_items = items_to_review)

				if(request.method == "POST"):
					form = ReviewForm(items_to_review, request.POST)
					if form.is_valid():
						review = form.save(commit = False)
						review.save()
						items_to_review.exclude(itemID = review.item)
						context_dict['items_to_review'] = items_to_review

						rating = 0
	
						if reviews_seller:
							for review in list(reviews_seller):
								rating += review.rating
							rating = rating/len(reviews_seller)

						return HttpResponseRedirect(reverse('tailored:show_seller_profile',
								kwargs = {'seller_username': seller_username}))
					else:
						print(form.errors)

				context_dict['form'] = form
				return render(request, "tailored/Sprofile.html", context_dict)
		finally:
			return render(request, 'tailored/Sprofile.html', context_dict)
	return render(request, 'tailored/Sprofile.html', context_dict)


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
			search = search.split(" ")
			searchS = "_".join(search)
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

	else :
		render(request, 'tailored/index.html', context_dict)


def home_page(request):
	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories

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