import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
											"tailored_project.settings")

import django
django.setup()
from tailored.models import Category, Item, Section, Size

def populate():

	# Instances of items
	T_Shirt_M = {"title": "Maison Margiela T-Shirt", "price": 60, "description" : "Slightly but still in good condition. Amazing quality",
				"sold" : False, "dailyVisits": 30, "size": "S", "itemPic": "item_images/MaisonShirt.jpg"}

	T_Shirt_W = {"title": "Red shirt", "price": 20, "description" : "Brand new red shirt, only selling because it´s the wrong size. Good quality",
				"sold" : False, "dailyVisits": 17, "size": "M", "itemPic":  "item_images/RedShirt.jpg"}

	T_Shirt_K = {"title": "Blue shirt", "price": 8, "description" : "Second hand shirt. Has been used often. Still in good condition",
				"sold" : False, "dailyVisits": 30, "size": "L", "itemPic": "item_images/BlueShirt.jpg"}

	Trousers_M = {"title": "Blue jeans", "price": 15, "description" : "Never used before. Good quality jeans.",
				"sold" : False, "dailyVisits": 16, "size": "S", "itemPic": "item_images/BlueJeans.jpg"}

	Trousers_W = {"title": "Ripped jeans", "price": 5, "description" : "Heavily used jeans. Not great quality but selling it for cheap.",
				"sold" : False, "dailyVisits": 0, "size": "M", "itemPic": "item_images/RippedJeans.jpg"}

	Trousers_K = {"title": "Black Levi jeans", "price": 30, "description" : "Second hand jeans. Have been used slighly. Selling because closet is full.",
				"sold" : False, "dailyVisits": 20, "size": "XL", "itemPic": "item_images/LeviJeans.jpg"}

	Jacket_M = {"title": "Nike Jacket", "price": 9, "description" : "Has been slightly used. Selling because closet is full",
				"sold" : False, "dailyVisits": 10, "size": "S", "itemPic": "item_images/NikeJacket.jpg"}
		
	Jacket_W = {"title": "American vintage jacket", "price": 20, "description" : "Never used before, amazing quality",
				"sold" : False, "dailyVisits": 4, "size": "M", "itemPic": "item_images/AmericanVintage.jpg"}
		
	Jacket_K = {"title": "Red Coat", "price": 10, "description" : "Basic red coat for kids. Very warm and cozy. Has been used slighly.",
				"sold" : False, "dailyVisits": 6, "size": "XXL", "itemPic": "item_images/RedCoat.jpg"}

	# List of items
	items = [T_Shirt_M, T_Shirt_W, T_Shirt_K, Trousers_M, Trousers_W, Trousers_K, Jacket_M, Jacket_W, Jacket_K]
	


	# List of sections
	sections = [{"title": "Men"}, {"title": "Women"}, {"title": "Kids"}]

	# List of categories
	categories = [{"title": "T-Shirts"}, {"title": "Trousers"}, {"title": "Jackets"}]

	# List of instances of sections
	sections_instances = []
	for section in sections:
		sections_instances.append(add_section(section["title"]))

	# List of instances of categories
	categories_instances = []
	for category in categories:
		categories_instances.append(add_category(category["title"]))

	for item_data in items:
		itemSize = add_size(item_data["size"])
	
		add_item(item_data["title"], item_data["price"], item_data["description"],
				item_data["sold"], item_data["dailyVisits"], itemSize,
				categories_instances[int(items.index(item_data)/len(categories_instances) % len(categories_instances))],
				sections_instances[items.index(item_data) % len(sections_instances)],
				item_data["itemPic"])

						
def add_item(title, price, description, sold, dailyVisits, size, category, section, itemPic):
	"""Adds a new item with the given title, price, description, sold, daily visits, size, category 
		and section to the database."""
	item = Item.objects.get_or_create(title = title, price = price, description = description,
									sold = sold, dailyVisits = dailyVisits, size = size, category = category, section = section, itemPic = itemPic)[0]
	return item

def add_category(title):
	"""Adds a new category with the given title to the database."""
	category = Category.objects.get_or_create(title = title)[0]
	category.save()
	return category

def add_section(title):
	"""Adds a new section with the given title to the database."""
	section = Section.objects.get_or_create(title = title)[0]
	section.save()
	return section

def add_size(title):
	size = Size.objects.get_or_create(title = title)[0]
	size.save()
	return size

if __name__ == "__main__":
	print("Starting population script...")
	populate()