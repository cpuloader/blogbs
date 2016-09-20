#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from blog.views import PostsListView, PostDetailView, PostCreateView

urlpatterns = [
    url(r'^$', PostsListView.as_view(), name='list'), 
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'), 
    url(r'^post/add/$', permission_required("blog.add_post")(PostCreateView.as_view()), name='post_add'),
]