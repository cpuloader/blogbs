#coding: utf-8
from django.conf.urls import url

from .views import EnterTextView, ShowLinkView, ShowTextView

urlpatterns = [
    url(r'^$', EnterTextView.as_view(), name='secret'), 
    url(r'^makelink/$', ShowLinkView.as_view(), name='link_ready'),
    url(r'^temp/(?P<key>.+)$', ShowTextView.as_view(), name='show_secret'),
]