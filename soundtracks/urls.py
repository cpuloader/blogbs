#coding: utf-8
from django.urls import re_path
from django.contrib.auth.decorators import permission_required

from soundtracks.views import TrackList, TrackDetail, TrackCreate, TrackDelete, track_create, \
               TrackUpdate, CommentCreate, CommentDelete, player_script, player_comments

urlpatterns = [
    re_path(r'^$', TrackList.as_view(), name='track_list'), 
    re_path(r'^(?P<pk>\d+)/$', TrackDetail.as_view(), name='track_detail'), 
    re_path(r'^track/add/$', permission_required("soundtracks.add_track")(TrackCreate.as_view()), name='track_add'),
    #url(r'^track/add/$', permission_required("soundtracks.add_track")(track_create), name='track_add'),
    re_path(r'^(?P<pk>\d+)/edit/$', permission_required("soundtracks.change_track")(TrackUpdate.as_view()), name = "track_edit"),
    re_path(r'^(?P<pk>\d+)/delete/$', permission_required("soundtracks.delete_track")(TrackDelete.as_view()), name = "track_delete"),
    re_path(r'^(?P<pk>\d+)/comment/add/$', permission_required("soundtracks.add_trackcomment")(CommentCreate.as_view()), name='track_comment_add'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$', permission_required("soundtracks.delete_trackcomment")(CommentDelete.as_view()), name='track_comment_delete'),
    re_path(r'^player.js$', player_script, name='player_script'),
    re_path(r'^comments.js$', player_comments, name='comments_script'),
]