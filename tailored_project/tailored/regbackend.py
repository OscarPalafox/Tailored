from registration.backends.simple.views import RegistrationView
from registration.models import RegistrationProfile
from tailored.models import UserProfile
from tailored.forms import UserProfileForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from PIL import Image
from os import path

class MyRegistrationView(RegistrationView):
	"""This class modifies the forms from the registration-django-redux app to implement the fields
	we have added in the models."""
	form_class = UserProfileForm

	def register(self, form_class):
		"""This function overrides the register function from RegistrationView."""
		user = super(MyRegistrationView, self).register(form_class)
		user.first_name = form_class.cleaned_data['first_name']
		user.last_name = form_class.cleaned_data['last_name']
		user = RegistrationProfile.objects.create_inactive_user(site = None, new_user = user)

		# Create our user profile and fill the details.
		user_profile = UserProfile()
		user_profile.user = user
		
		if not form_class.cleaned_data['picture']:
			# Handle when the user does not upload a profile picture
			image = Image.open(path.dirname(path.dirname(path.abspath(__file__))) + static('images/profile.jpg'))
			
			if image.mode != "RGB":
				image = image.convert("RGB")

			output = BytesIO()
			image.save(output, 'JPEG', quality = 100)
			output.seek(0)

			file_system = FileSystemStorage(settings.MEDIA_ROOT + '/profile_images/')
			filename = file_system.save('profile.jpg', output)
			file_url = file_system.url(filename)

			user_profile.picture = file_url.replace('/media', 'profile_images', 1)
		else:
			user_profile.picture = form_class.cleaned_data['picture']
		
		# Clean up the postcode
		input_postcode = form_class.cleaned_data['postcode'].replace(' ', '').upper()
		user_profile.postcode = input_postcode[:-3] + ' ' + input_postcode[-3:]
		user_profile.phone = form_class.cleaned_data['phone']

		user_profile.save()
		return user_profile

	def get_form_class(self):
		return UserProfileForm