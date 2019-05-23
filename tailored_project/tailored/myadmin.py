from django.contrib import admin
from tailored.models import Item
from registration.models import RegistrationProfile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy
from registration.users import UsernameField


class ItemAdmin(admin.ModelAdmin):
	"""This is a class that modifies the admin page of the Item model."""
	list_display = ('title', 'seller', 'section', 'category', 'sold_to')
	readonly_fields = ('itemID', )


class ReviewAdmin(admin.ModelAdmin):
	"""This is a class that modifies the admin page of the Review model."""

	def get_item_seller(self, review):
		"""This function returns the seller of the given review."""
		return review.item.seller

	get_item_seller.admin_order_field  = 'item__seller'
	get_item_seller.short_description = 'Seller'

	list_display = ('item', 'get_item_seller','rating', 'datePosted')


class UserProfileAdmin(admin.ModelAdmin):
	"""This is a class that modifies the admin page of the UserProfile model."""
	list_display = ('user', 'get_user_first', 'get_user_last', 'postcode')

	def get_user_first(self, user_profile):
		"""This function returns the first name of the given user profile."""
		return user_profile.user.first_name

	get_user_first.admin_order_field  = 'user__first_name'
	get_user_first.short_description = 'First Name'

	def get_user_last(self, user_profile):
		"""This function returns the last name of the given user profile."""
		return user_profile.user.last_name

	get_user_last.admin_order_field  = 'user__last_name'
	get_user_last.short_description = 'Last Name'


class MyRegistrationAdmin(admin.ModelAdmin):
	"""This is a class that modifies the admin page of the Registration model."""
	actions = ['activate_users', 'resend_activation_email']
	list_display = ('user', 'activation_key_expired')
	search_fields = (f'user__{UsernameField()}',
					 'user__first_name', 'user__last_name')

	def activate_users(self, request, queryset):
		"""Activates the selected users, if they are not already activated."""

		site = get_current_site(request)
		for profile in queryset:
			RegistrationProfile.objects.activate_user(profile.activation_key, site)
	
	activate_users.short_description = ugettext_lazy("Activate users")

	def resend_activation_email(self, request, queryset):
		"""Re-sends activation emails for the selected users.Note that this will 
		*only* send activation emails for users who are eligible to activate;
		emails will not be sent to users whose activation keys have expired or 
		who have already activated."""

		site = get_current_site(request)
		
		for profile in queryset:
			user = profile.user
			RegistrationProfile.objects.resend_activation_mail(user.email, site, request)

	resend_activation_email.short_description = ugettext_lazy("Re-send activation emails")