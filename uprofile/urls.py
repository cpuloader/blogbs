#coding: utf-8
from django.urls import re_path

from .views import user_create, user_profile, user_update

urlpatterns = [
    re_path(r'^user/add/$', user_create, name='user_add'),
    re_path(r'^user/profile/(?P<pk>\d+)$', user_profile, name='user_profile'),
    re_path(r'^user/profile/edit/(?P<pk>\d+)$', user_update, name='user_profile_edit')
]