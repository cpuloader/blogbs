# -*- coding: utf8 -*-
from django.urls import re_path

from .views import CommandReceiveView

urlpatterns = [
    re_path(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]