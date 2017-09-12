from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from ans.views import *

urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', include('ans.urls')),
    url(r'^logout/$', logout_view, name='logout'),


]

