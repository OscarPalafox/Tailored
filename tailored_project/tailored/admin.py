from django.contrib import admin
from tailored.models import Section, Category, Item, UserProfile, Review, Size
from registration.models import RegistrationProfile
from tailored.myadmin import ItemAdmin, MyRegistrationAdmin


admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)

admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Size)
admin.site.unregister(RegistrationProfile)
admin.site.register(RegistrationProfile, MyRegistrationAdmin)