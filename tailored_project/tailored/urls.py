from django.conf.urls import url
from tailored import views

app_name = 'tailored'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^items/$', views.items, name = 'items'),
	url(r'^add_category/$', views.add_category, name = 'add_category'),
	url(r'^section/(?P<title>[-\w]+)/$', views.show_section, name = 'show_section'),
	url(r'^category/(?P<title>[-\w]+)/$', views.show_category, name = 'show_category'),
	url(r'^home/$', views.home_page, name = 'home_page'),
	url(r'^search/$', views.search_bar, name = 'search')
]