from django.conf.urls import include,patterns, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/', include('lists.urls')),     
    # url(r'^admin/', include(admin.site.urls)),
)

