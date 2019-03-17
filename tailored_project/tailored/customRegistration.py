from registration.backends.simple.views import RegistrationView

from tailored.models import UserProfile
from tailored.forms import UserProfileForm

class MyRegistrationView(RegistrationView):
	form_class = UserProfileForm

	def register(self, form_class):
		user = super(MyRegistrationView, self).register(form_class)
		user.first_name = form_class.cleaned_data['first_name']
		user.last_name = form_class.cleaned_data['last_name']
		user.save()

		user_profile = UserProfile()
		user_profile.user = user
		user_profile.picture = form_class.cleaned_data['picture']
		user_profile.postcode = form_class.cleaned_data['postcode']
		user_profile.phone = form_class.cleaned_data['phone']
		user_profile.rating = 0

		user_profile.save()
		return user_profile


	def get_form_class(self):
		return UserProfileForm

	def get_success_url(self, user):
		return 'tailored:index'