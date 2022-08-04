#coding: utf-8
from django.urls import re_path
from django.contrib.auth.decorators import permission_required

from blog.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, \
           CommentCreate, CommentRemove, post_list_json, posts_load_script, test_redirect

urlpatterns = [
    re_path(r'^$', PostList.as_view(), name='list'),
    re_path(r'^json/(?P<page>[0-9]+)/$', post_list_json, name='list-json'), 
    re_path(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='post_detail'), 
    re_path(r'^post/add/$', permission_required("blog.add_post")(PostCreate.as_view()), name='post_add'),
    re_path(r'^edit/(?P<pk>\d+)$', permission_required("blog.change_post")(PostUpdate.as_view()), name = "post_edit"),
    re_path(r'^delete/(?P<pk>\d+)$', permission_required("blog.delete_post")(PostDelete.as_view()), name = "post_delete"),
    re_path(r'^comment/(?P<pk>\d+)/add/$', permission_required("blog.add_comment")(CommentCreate.as_view()), name='comment_add'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$', permission_required("blog.delete_comment")(CommentRemove.as_view()), name='comment_remove'),
    re_path(r'^posts_load_script.js$', posts_load_script, name='posts_load'),
    re_path(r'^test_redirect$', test_redirect, name='test_redirect'),
]