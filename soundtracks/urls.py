#coding: utf-8
from django.conf.urls import url

from soundtracks.views import TrackListView, player_script

urlpatterns = [
    url(r'^$', TrackListView.as_view(), name='tracks_list'), 
    url(r'^player.js$', player_script, name='player_script'),
]