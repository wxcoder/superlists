from django.conf.urls import url
from lists import views
#from django.contrib import admin

urlpatterns = [
	url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),  

]

