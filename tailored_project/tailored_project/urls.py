from django.conf.urls import url
from django.contrib import admin
from tailored import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'index/$', views.home_page, name='home_page'),
	url(r'^tailored/search/$', views.search_bar, name='search'),

	url(r'^tailored/categories/$', views.categories, name='categories'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
