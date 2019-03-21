from django.conf.urls import url
from tailored import views

app_name = 'tailored'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^items/$', views.items, name = 'items'),
	url(r'^section/(?P<title>[-\w]+)/$', views.show_section, name = 'show_section'),
	url(r'^user_profile/$', views.add_item, name = "add_item"),
	url(r'^trending/$', views.trending, name = "trending"),
	url(r'^category/(?P<title>[-\w]+)/$', views.show_category, name = 'show_category'),
	url(r'^index/$', views.home_page, name = 'home_page'),
	url(r'^search/new/(?P<search>[-\w]+)/$', views.new_in, name = 'new_in'),
	url(r'^home/$', views.home_page, name = 'home_page'),
	url(r'^tailored/$', views.search_bar, name = 'home_page'),
	url(r'^search/$', views.search_bar, name = 'search'),
	url(r'^search/(?P<search>[-\w]+)/$', views.search_bar, name = 'search'),
	#url(r'^leave_review/$', views.leave_review, name = 'leave_review'),
	url(r'^profile/(?P<seller_username>[-\w]+)/$', views.show_seller_profile, name = 'show_seller_profile'),
	url(r'^item/(?P<itemID>[-\w]+)/$', views.show_item, name = 'show_item'),
	url(r'^add_item/$', views.add_item, name = 'add_item'),
	url(r'^user_profile/edit/$', views.edit_profile, name = 'edit_profile'),
	url(r'^edit/(?P<itemID>[-\w]+)/$', views.edit_item, name = 'edit_item')

]