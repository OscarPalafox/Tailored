import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tailored_project.settings')
import django
django.setup()
from tailored.models import Category, Item, Section, Size, UserProfile, Review
from registration.models import RegistrationProfile
from django.contrib.auth.models import User
from datetime import date

def populate():
	# Users
	user1 = {'username': 'AndrewI', 'email': 'andrew@gmail.com', 'password': 'AndrewWorld2010',
			'first_name': 'Andrew', 'last_name': 'Iniesta', 'picture': 'profile_images/AndrewI.jpg',
			'postcode': 'EC2R 8AH', 'phone': '00442078391377'}

	user2 = {'username': 'CharlesP', 'email': 'charles@gmail.com', 'password': 'CharlesWorld2010',
			'first_name': 'Charles', 'last_name': 'Puyol', 'picture': 'profile_images/CharlesP.jpg',
			'postcode': 'W1D 1AN', 'phone': '00442073726258'}

	user3 = {'username': 'XavierH', 'email': 'xavier@gmail.com', 'password': 'XavierWorld2010',
			'first_name': 'Xavier', 'last_name': 'Hernandez', 'picture': 'profile_images/XavierH.jpg',
			'postcode': 'SO17 1BJ', 'phone': '0034687254448'}

	user4 = {'username': 'IkerC', 'email': 'Iker@gmail.com', 'password': 'IkerWorld2010',
			'first_name': 'Iker', 'last_name': 'Casillas', 'picture': 'profile_images/placeholder.jpg',
			'postcode': 'SA6 7JL', 'phone': '00442056343414'}

	# List of users
	users = [user1, user2, user3, user4]

	# List of user profile instances
	user_profiles_instances = []

	for user_data in users:
		user_profiles_instances.append(add_user_profile(user_data['username'], user_data['email'],
										user_data['password'], user_data['first_name'], 
										user_data['last_name'], user_data['picture'],
										user_data['postcode'], user_data['phone']))


	# Items data
	T_Shirt_M = {'title': 'Maison Margiela T-Shirt', 'price': 60,
					'description' : 'Slightly but still in good condition. Amazing quality',
					'sold_to' : user_profiles_instances[0],
					'seller': user_profiles_instances[1],
					'dailyVisits': 30, 'size': 'S', 'picture': 'item_images/MaisonShirt.jpg',
					'datePosted': date(2019, 1, 20)}

	T_Shirt_W = {'title': 'Red shirt', 'price': 20,
					'description' : "Brand new red shirt, only selling because it's the wrong size. Good quality",
					'sold_to' : user_profiles_instances[1],
					'seller': user_profiles_instances[2],
					'dailyVisits': 17, 'size': 'M', 'picture':  'item_images/RedShirt.jpg',
					'datePosted': date(2019, 2, 28)}

	T_Shirt_K = {'title': 'Blue shirt', 'price': 8,
					'description' : 'Second hand shirt. Has been used often. Still in good condition',
					'sold_to' : None, 'seller': user_profiles_instances[0], 'dailyVisits': 30, 'size': 'L',
					'picture': 'item_images/BlueShirt.jpg'}

	Trousers_M = {'title': 'Blue jeans', 'price': 15,
					'description' : 'Never used before. Good quality jeans.', 'sold_to' : None,
					'seller': user_profiles_instances[3],
					'dailyVisits': 16, 'size': 'XS', 'picture': 'item_images/BlueJeans.jpg'}

	Trousers_W = {'title': 'Ripped jeans', 'price': 5,
					'description' : 'Heavily used jeans. Not great quality but selling it for cheap.',
					'sold_to' : user_profiles_instances[2],
					'seller': user_profiles_instances[3],
					'dailyVisits': 0, 'size': 'M', 'picture': 'item_images/RippedJeans.jpg', 
					'datePosted': date(2019, 2, 10)}

	Trousers_K = {'title': 'Black Levi jeans', 'price': 30,
					'description' : 'Second hand jeans. Have been used slighly. Selling because closet is full.',
					'sold_to' : user_profiles_instances[3],
					'seller': user_profiles_instances[0],
					'dailyVisits': 20, 'size': 'XL', 'picture': 'item_images/LeviJeans.jpg',
					'datePosted': date(2019, 3, 14)}

	Jacket_M = {'title': 'Nike Jacket', 'price': 9,
				'description' : 'Has been slightly used. Selling because closet is full',
				'sold_to' : user_profiles_instances[2],
				'seller': user_profiles_instances[1],
				'dailyVisits': 10, 'size': 'S', 'picture': 'item_images/NikeJacket.jpg'}
		
	Jacket_W = {'title': 'American vintage jacket', 'price': 20,
				'description' : 'Never used before, amazing quality', 'sold_to' : None, 
				'seller': user_profiles_instances[2], 'dailyVisits': 4,
				'size': 'M', 'picture': 'item_images/AmericanVintage.jpg',}

	Jacket_K = {'title': 'Red Coat', 'price': 10,
				'description' : 'Basic red coat for kids. Very warm and cozy. Has been used slighly.',
				'sold_to' : user_profiles_instances[3],
				'seller': user_profiles_instances[0],
				'dailyVisits': 6, 'size': 'XXL', 'picture': 'item_images/RedCoat.jpg',
				'datePosted': date(2018, 12, 23)}

	# List of items
	items = [T_Shirt_M, Trousers_W, Jacket_K, T_Shirt_W, T_Shirt_K, Trousers_M, Trousers_K, Jacket_M, Jacket_W]

	
	# List of sections
	sections = [{'title': 'Men'}, {'title': 'Women'}, {'title': 'Kids'}]

	
	# List of categories
	categories = [{'title': 'T-Shirts'}, {'title': 'Trousers'}, {'title': 'Jackets'}]

	
	# List of instances of sections
	sections_instances = []
	for section in sections:
		sections_instances.append(add_section(section['title']))

	
	# List of instances of categories
	categories_instances = []
	for category in categories:
		categories_instances.append(add_category(category['title']))


	# List of instances of items
	item_instances = []
	for item_data in items:
		user_profiles_instances_copy = [user for user in user_profiles_instances if user != item_data['sold_to']]
		itemSize = add_size(item_data['size'])
	
		item_instances.append(add_item(item_data['title'], item_data['price'], item_data['description'],
				item_data['sold_to'], item_data['dailyVisits'], itemSize,
				categories_instances[int(items.index(item_data)/len(categories_instances) 
																% len(categories_instances))],
				sections_instances[items.index(item_data) % len(sections_instances)],
				item_data['picture'], item_data['seller'],
				item_data.get('datePosted', date.today())))

	# Reviews data
	review1 = {'review_text': 'The seller was punctual and everything went great.', 'rating': 5, 
				'datePosted': date(2019, 1, 21)}

	review2 = {'review_text': '''The seller showed up two hours late and the piece of 
				clothing was dirty. He even tried to raise the price, not recommended.''', 'rating': 1,
				'datePosted': date(2019, 3, 14)}

	review3 = {'review_text': 'The seller was not punctual but everything went as expected.', 'rating': 3,
				'datePosted': date(2019, 1, 11)}

	# List of reviews
	reviews = [review1, review2, review3]

	for item in item_instances:
		if item_instances.index(item) % 4 == 0:
			add_review(item, reviews[int(item_instances.index(item)/4)]['rating'],
						reviews[int(item_instances.index(item)/4)]['review_text'],
						reviews[int(item_instances.index(item)/4)]['datePosted'])
			item.seller.rating = reviews[int(item_instances.index(item)/4)]['rating']
			item.seller.save()

						
def add_item(title, price, description, sold_to, dailyVisits, size, category, section, picture, seller, datePosted):
	'''Adds a new item with the given parameters.'''
	item = Item.objects.get_or_create(title = title, price = price, description = description,
									sold_to = sold_to, dailyVisits = dailyVisits, size = size,
									category = category, section = section, picture = picture, seller = seller,
									datePosted = datePosted)[0]
	item.save()
	return item


def add_category(title):
	'''Adds a new category with the given title to the database.'''
	category = Category.objects.get_or_create(title = title)[0]
	category.save()
	return category


def add_section(title):
	'''Adds a new section with the given title to the database.'''
	section = Section.objects.get_or_create(title = title)[0]
	section.save()
	return section


def add_size(title):
	'''Adds a new size with the given title to the database.'''
	size = Size.objects.get_or_create(title = title)[0]
	size.save()
	return size


def add_user_profile(username, email, password, first_name, last_name, picture, postcode, phone):
	'''Adds a new user profile with the given parameters.'''
	user = User.objects.create_user(username = username, email = email, password = password,
									first_name = first_name, last_name = last_name)
	user = RegistrationProfile.objects.create_inactive_user(site = None, new_user = user, send_email = False)
	RegistrationProfile.objects.activate_user(activation_key = RegistrationProfile.objects.get(user = user
												).activation_key, site = None)
	
	user_profile = UserProfile()
	user_profile.user = user
	user_profile.picture = picture
	
	user_profile.postcode = postcode
	user_profile.phone = phone
	user_profile.rating = 0

	user_profile.save()

	return user_profile


def add_review(item, rating, review_text, datePosted):
	'''Adds a new review to the given item with the given parameters.'''
	review_text_formatted = review_text.replace('\t', '').replace('\n', '')
	review = Review.objects.get_or_create(item = item, rating = rating, review_text = review_text_formatted,
											datePosted = datePosted)[0]
	review.save()
	return review

if __name__ == '__main__':
	print('Starting population script...')
	populate()
	print('Population script executed successfully, database populated.')