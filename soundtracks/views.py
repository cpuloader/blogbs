from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from .models import Track

class JavaScriptView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = "application/javascript"
        return super(JavaScriptView, self).render_to_response(
            context, **response_kwargs)

player_script = JavaScriptView.as_view(template_name="soundtracks/player.js")

class TrackListView(ListView): 
    model = Track
    fields = "__all__"
    template_name = "soundtracks/tracklist.html"
    success_url = reverse_lazy("tracks_list")

    #def get_context_data(self, **kwargs):
    #    context = super(TracksListView, self).get_context_data(**kwargs)
    #    context['tracks'] = Track.objects.all()
    #    return context

