#coding: utf-8
from django.urls import re_path

from .views import EnterTextView, ShowLinkView, your_file#ShowTextView

urlpatterns = [
    re_path(r'^$', EnterTextView.as_view(), name='secret'), 
    re_path(r'^makelink/$', ShowLinkView.as_view(), name='link_ready'),
    #url(r'^temp/(?P<key>.+)$', ShowTextView.as_view(), name='show_secret'),
    re_path(r'^temp/(?P<key>.+)$', your_file, name='show_secret'),
]