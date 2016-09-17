#coding: utf-8
from django.conf.urls import url

from blog.views import PostsListView, PostDetailView, PostCreateView#, myscript

urlpatterns = [
    url(r'^$', PostsListView.as_view(), name='list'), 
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'), 
    url(r'^post/add/$', PostCreateView.as_view(), name='post_add'),
   #url(r'^$', myscript, name = "my_script"),
]