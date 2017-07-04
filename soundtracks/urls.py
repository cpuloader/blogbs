#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from soundtracks.views import TrackList, TrackDetail, TrackCreate, TrackDelete, \
               TrackUpdate, CommentCreate, CommentDelete, player_script, player_comments

urlpatterns = [
    url(r'^$', TrackList.as_view(), name='track_list'), 
    url(r'^(?P<pk>\d+)/$', TrackDetail.as_view(), name='track_detail'), 
    url(r'^track/add/$', permission_required("soundtracks.add_track")(TrackCreate.as_view()), name='track_add'),
    url(r'^(?P<pk>\d+)/edit/$', permission_required("soundtracks.change_track")(TrackUpdate.as_view()), name = "track_edit"),
    url(r'^(?P<pk>\d+)/delete/$', permission_required("soundtracks.delete_track")(TrackDelete.as_view()), name = "track_delete"),
    url(r'^(?P<pk>\d+)/comment/add/$', permission_required("soundtracks.add_trackcomment")(CommentCreate.as_view()), name='track_comment_add'),
    url(r'^comment/(?P<pk>\d+)/remove/$', permission_required("soundtracks.delete_trackcomment")(CommentDelete.as_view()), name='track_comment_delete'),
    url(r'^player.js$', player_script, name='player_script'),
    url(r'^comments.js$', player_comments, name='comments_script'),
]