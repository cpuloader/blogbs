#coding: utf-8
from django.conf.urls import url

from carousel.views import CarouselView

urlpatterns = [
    url(r'^$', CarouselView.as_view(), name='carousel_name'), 
]