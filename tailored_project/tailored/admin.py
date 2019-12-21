from django.contrib import admin
from tailored.models import Section, Category, Item, UserProfile, Review, Size
from registration.models import RegistrationProfile
from tailored.myadmin import ItemAdmin, ReviewAdmin, UserProfileAdmin, MyRegistrationAdmin

# Models to register in the admin page
admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Size)

# Remove the default RegistrationProfile
admin.site.unregister(RegistrationProfile)

# Add the RegistrationProfile with the custom page
admin.site.register(RegistrationProfile, MyRegistrationAdmin)