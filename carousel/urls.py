#coding: utf-8
from django.urls import re_path

from carousel.views import CarouselView

urlpatterns = [
    re_path(r'^$', CarouselView.as_view(), name='carousel_name'), 
]