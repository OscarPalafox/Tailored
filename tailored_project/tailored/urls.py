from django.conf.urls import url
from tailored import views

app_name = "tailored"

urlpatterns = [
	url(r'^section/(?P<title>[-\w]+)/$', views.show_section, name = 'show_section'),
	url(r'^category/(?P<title>[-\w]+)/$',
        views.show_category, name='show_category'),
]