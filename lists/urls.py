from django.conf.urls import url
from lists import views
#from django.contrib import admin

urlpatterns = [
	url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),
    url(r'^(\d+)/share$', views.shared_lists, name='shared_lists')  

]

