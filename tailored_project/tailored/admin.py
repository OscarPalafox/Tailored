from django.contrib import admin
from tailored.models import Section, Category, Item, UserProfile, Review, Size

#class PersonAdmin(admin.ModelAdmin):
	#readonly_fields = ('itemID', )

admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Item)#, PersonAdmin)

admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Size)


