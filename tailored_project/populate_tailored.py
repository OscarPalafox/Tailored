import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "tailored_project.settings")

import django
django.setup()
from rango.models import Category, Item, Section

def populate():
    
    tops_M = [{"itemName": "Blue shirt", "price": 10, "description" : "Niko is the best "
               , "datePosted": , "sold" : False, "dailyVisits": 100, "size": s}]

    tops_F = [{"itemName": "Red shirt",
               "price": 5}]

    tops_K = [{"itemName": "Green shirt",
               "price": 7}]

    bottoms_M = [{"itemName": "Jeans",
               "price": 15}]

    bottoms_F = [{"itemName": "Ripped Jeans",
               "price": 20}]

    bottoms_K = [{"itemName": "Jeans",
               "price": 8}]
    jackets_M =[{"itemName": "Jeans",
               "price": 8}]
    
    jackets_F =[{"itemName": "Jeans",
               "price": 8}]
    
    jackets_K =[{"itemName": "Jeans",
               "price": 8}]
    
    section_M = {"Tops": tops_M, "Bottoms": bottoms_M, "Jackets":jackets_M}
    section_F = {"Tops": tops_F, "Bottoms": bottoms_F, "Jackets":jackets_F}
    section_K = {"Tops": tops_K, "Bottoms": bottoms_K, "Jackets":jackets_K}

    gender_cats = {"Men": section_M, "Women": section_F, "Kids": section_K }
    for section in gender_cats:
        s = add_section(section)
        for cat in gender_cats[section]:
            c = add_cat(s, cat)
            for item in sections[section][cat]:
                add_item(c, item["itemName"], item["price"])
            
def add_item(cat,itemName, price, description, datePosted, sold, dailyVisits, size ):
    i = Item.objects.get_or_create(category = cat, itemName=itemName)[0]
    i.price = price
    i.description = description
    i.datePosted = datePosted
    i.sold = sold
    i.dailyVisits = dailyVisits
    i.size = size
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
    
        
