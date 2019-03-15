import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
											"tailored_project.settings")

import django
django.setup()
from tailored.models import Category, Item, Section

def populate():

	T_Shirt_M = {"name": "Blue shirt", "price": 10, "description" : "Niko is the best ", 
					"sold" : False, "dailyVisits": 100, "size": "S", "category": "T-Shirt",
								"section": "Men"}

	T_Shirt_W = {"name": "Blue shirt", "price": 10, "description" : "Niko is the best ",
								"sold" : False, "dailyVisits": 100, "size": "S", "category": "T-Shirt",
								"section": "Women"}

	T_Shirt_K = {"name": "Blue shirt", "price": 10, "description" : "Niko is the best ",
								"sold" : False, "dailyVisits": 100, "size": "S", "category": "T-Shirt",
								"section": "Kids"}

	Trousers_M = {"name": "Jeans", "price": 10, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 100, "size": "S", "category": "Trousers",
								"section": "Men"}

	Trousers_W = {"name": "Jeans", "price": 10, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 100, "size": "S", "category": "Trousers",
								"section": "Women"}

	Trousers_K = {"name": "Jeans", "price": 10, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 100, "size": "S", "category": "Trousers",
								"section": "Kids"}

	Jacket_M = {"name": "Blue Coat", "price": 10, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 100, "size": "S", "category": "Jackets",
								"section": "Men"}
		
	Jacket_W = {"name": "Blue Coat", "price": 10, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 100, "size": "S", "category": "Jackets",
								"section": "Women"}
		
	Jacket_K = {"name": "Blue Coat", "price": 10, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 100, "size": "S", "category": "Jackets",
								"section": "Kids"}

	items = [T_Shirt_M, T_Shirt_W, T_Shirt_K, Trousers_M, Trousers_W, Trousers_K, Jacket_M, Jacket_W, Jacket_K]
		
	sections = [{"title": "Men"}, {"title": "Women"}, {"title": "Kids"}]

	categories = [{"title": "T-Shirt"}, {"title": "Trousers"}, {"title": "Jackets"}]

	sections_instances = []
	for section in sections:
		sections_instances.append(add_section(section["title"]))

	categories_instances = []
	for category in categories:
		categories_instances.append(add_category(category["title"]))

	for item_data in items:
		add_item(item_data["name"], item_data["price"], item_data["description"],
				item_data["sold"], item_data["dailyVisits"], item_data["size"],
				categories_instances[int(items.index(item_data)/len(categories_instances) % len(categories_instances))],
				sections_instances[items.index(item_data) % len(sections_instances)])

						
def add_item(name, price, description, sold, dailyVisits, size, category, section):
	item = Item.objects.get_or_create(name = name, price = price, description = description,
									sold = sold, dailyVisits = dailyVisits, size = size, category = category, section = section)[0]
	return item

def add_category(title):
	category = Category.objects.get_or_create(title = title)[0]
	category.save()
	return category

def add_section(title):
	section = Section.objects.get_or_create(title = title)[0]
	section.save()
	return section

if __name__ == "__main__":
	print("Starting population script...")
	populate()