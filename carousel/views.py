from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

from .models import Picture

class CarouselView(TemplateView): 
    model = Picture
    fields = "__all__"
    template_name = "carousel/carousel.html"
    success_url = reverse_lazy("carousel_name")

    def get_context_data(self, **kwargs):
        context = super(CarouselView, self).get_context_data(**kwargs)
        context['pictures'] = Picture.objects.all()
        return context

