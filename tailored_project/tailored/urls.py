from django.conf.urls import url
from tailored import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = "tailored"

urlpatterns = [
	url(r'^section/(?P<title>[-\w]+)/$', views.show_section, name = 'show_section'),
	url(r'^category/(?P<title>[-\w]+)/$',
        views.show_category, name='show_category'),
	url(r'^admin/', admin.site.urls),
	url(r'^index/$', views.home_page, name='home_page'),
	url(r'^tailored/search/$', views.search_bar, name='search'),
	url(r'add_item/$', views.add_item, name="add_item"),
]




