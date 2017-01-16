#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from blog.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, \
           CommentCreate, CommentRemove

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'), 
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='post_detail'), 
    url(r'^post/add/$', permission_required("blog.add_post")(PostCreate.as_view()), name='post_add'),
    url(r'^(?P<pk>\d+)/edit/$', permission_required("blog.change_post")(PostUpdate.as_view()), name = "post_edit"),
    url(r'^(?P<pk>\d+)/delete/$', permission_required("blog.delete_post")(PostDelete.as_view()), name = "post_delete"),
    #url(r'^user/add/$', UserCreate.as_view(), name='user_add'),
    url(r'^comment/(?P<pk>\d+)/add/$', permission_required("blog.add_comment")(CommentCreate.as_view()), name='comment_add'),
    url(r'^comment/(?P<pk>\d+)/remove/$', permission_required("blog.delete_comment")(CommentRemove.as_view()), name='comment_remove'),
]