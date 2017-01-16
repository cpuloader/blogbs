#coding: utf-8
from django.conf.urls import url

from .views import user_create, user_profile, user_update

urlpatterns = [
    url(r'^user/add/$', user_create, name='user_add'),
    url(r'^user/profile/(?P<pk>\d+)$', user_profile, name='user_profile'),
    url(r'^user/profile/edit/(?P<pk>\d+)$', user_update, name='user_profile_edit')
]