from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tailored import views
from tailored.customRegistration import MyRegistrationView
from tailored.forms import UserProfileForm

urlpatterns = [
	url(r'^', include('tailored.urls')),
	url(r'^register/$', MyRegistrationView.as_view(form_class = UserProfileForm), name = 'registration_register'),
	url(r'^', include('registration.backends.simple.urls')),
	url(r'^admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
