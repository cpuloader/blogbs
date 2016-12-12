#coding: utf-8
from django.conf.urls import url

from .views import enter_new_text, play_new_text, tplayer_script, pretext_script

urlpatterns = [
    url(r'^$', enter_new_text, name='speaker'), 
    url(r'^play/(?P<pk>\d+)$', play_new_text, name='play_text'),
    url(r'^tplayer.js$', tplayer_script, name='tplayer_script'),
    url(r'^pretext.js$', pretext_script, name='pretext_script'),
]