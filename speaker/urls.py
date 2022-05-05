#coding: utf-8
from django.urls import re_path

from .views import enter_new_text, play_new_text, tplayer_script, pretext_script

urlpatterns = [
    re_path(r'^new/(?P<autoplay>\w+)$', enter_new_text, name='speaker'), 
    re_path(r'^play/(?P<pk>\d+)$', play_new_text, name='play_text'),
    re_path(r'^tplayer.js$', tplayer_script, name='tplayer_script'),
    re_path(r'^pretext.js$', pretext_script, name='pretext_script'),
]