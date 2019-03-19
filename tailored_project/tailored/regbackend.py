from registration.backends.simple.views import RegistrationView
from registration.models import RegistrationProfile
from tailored.models import UserProfile
from tailored.forms import UserProfileForm

class MyRegistrationView(RegistrationView):
	"""This class modifies the forms from the registration-django-redux app to implement the fields
	we have added in the models."""
	form_class = UserProfileForm

	def register(self, form_class):
		# Override the register function from RegistrationView
		user = super(MyRegistrationView, self).register(form_class)
		user.first_name = form_class.cleaned_data['first_name']
		user.last_name = form_class.cleaned_data['last_name']
		user = RegistrationProfile.objects.create_inactive_user(site = None, new_user = user)
		# Create our user profile and fill the details.
		user_profile = UserProfile()
		user_profile.user = user
		
		if form_class.cleaned_data['picture'] == None:
			user_profile.picture = 'profile_images/placeholder.jpg'
		else:
			user_profile.picture = form_class.cleaned_data['picture']
		
		input_postcode = form_class.cleaned_data['postcode'].replace(' ', '').upper()
		user_profile.postcode = input_postcode[:-3] + ' ' + input_postcode[-3:]
		user_profile.phone = form_class.cleaned_data['phone']
		user_profile.rating = 0

		user_profile.save()
		return user_profile

	def get_form_class(self):
		return UserProfileForm