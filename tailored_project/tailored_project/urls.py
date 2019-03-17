from django.conf.urls import url
from django.contrib import admin
from tailored import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'index/$', views.home_page, name='home_page'),
	url(r'^tailored/search/$', views.search_bar, name='search'),
	url(r'^tailored/(?P<category>[\w\-]+)/$', views.search_bar, name='search'),
	url(r'^tailored/(?P<search>[\w\-]+)/(?P<category>[\w\-]+)/$', views.search_bar, name='search'),
	url(r'^tailored/(?P<search>[\w\-]+)//$', views.search_bar, name='search'),
		url(r'^tailored/(?P<search>[\w\-]+)/$', views.search_bar, name='search'),
	url(r'^tailored/$', views.search_bar, name='search'),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
