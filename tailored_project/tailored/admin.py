from django.contrib import admin
from tailored.models import Section, Category, Item, UserProfile, Review, Size

class ItemAdmin(admin.ModelAdmin):
	readonly_fields = ('itemID', )

"""class ReviewAdmin(admin.ModelAdmin):
	readonly_fields = ('reviewID', )"""

admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)

admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Size)


