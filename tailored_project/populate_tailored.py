import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "tailored_project.settings")

import django
django.setup()
from rango.models import Category, Item

def populate():

    shirt_M = [{"itemName": "Blue shirt",
               "price": 10}]

    shirt_F = [{"itemName": "Red shirt",
               "price": 5}]

    shirt_K = [{"itemName": "Green shirt",
               "price": 7}]

    pants_M = [{"itemName": "Jeans",
               "price": 15}]

    pants_F = [{"itemName": "Ripped Jeans",
               "price": 20}]

    pants_K = [{"itemName": "Jeans",
               "price": 8}]

    cat_M = {"Shirts": shirt_M, "Pants": pants_M}
    cat_F = {"Shirts": shirt_F, "Pants": pants_F}
    cat_K = {"Shirts": shirt_K, "Pants": pants_K}

    sections = {"Men": cat_M, "Women": cat_F, "Kids": cat_K}

    for section in sections:
        s = add_section(section)
        for cat in sections[section]:
            c = add_cat(s, section+" "+cat)
            for item in sections[section][cat]:
                add_item(c, item["itemName"], item["price"])
            
def add_item(cat,itemName, price):
    i = Item.objects.get_or_create(category = cat, itemName=itemName)[0]
    i.price = price
    i.save()
    return i

def add_cat(sec, title):
    c = Category.objects.get_or_create(section = sec, title = title)[0]
    c.save()
    return c

def add_section(name):
    s = Section.objects.get_or_create(name = name)[0]
    s.save()
    return s

if __name__ == "__main__":
    print("Starting population script...")
    populate()
    
        
