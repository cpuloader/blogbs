# coding: utf-8
import os
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from .models import Track, TrackComment
from .forms import TrackForm, TrackDeleteForm, CommentForm, CommentDeleteForm
from blog.views import JavaScriptView

player_script = JavaScriptView.as_view(template_name="soundtracks/player.js")
player_comments = JavaScriptView.as_view(template_name="soundtracks/comments.js")


class TrackList(ListView): 
    model = Track
    fields = "__all__"
    template_name = "soundtracks/tracklist.html"
    success_url = reverse_lazy("track_list")


class TrackDetail(DetailView):
    model = Track
    template_name = "soundtracks/track_detail.html"
    success_url = reverse_lazy("track_list")

    def get(self, request, *args, **kwargs):
        self.track = Track.objects.get(pk = self.kwargs["pk"])
        return super(TrackDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TrackDetail, self).get_context_data(**kwargs)
        user = self.request.user
        #print(user.username)
        #initial_data = {'parent_track': self.kwargs["pk"], 'author': user }
        context["comment_form"] = CommentForm() #initial = initial_data
        context["comment_delete_form"] = CommentDeleteForm(initial = {'parent_track': self.kwargs["pk"]})
        context["comments"] = self.track.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        return redirect(reverse("track_list"))

def track_create(request): 
    if request.method == 'POST':
        track_form = TrackForm(request.POST, request.FILES)
        if track_form.is_valid():
            instance = Track(author=request.user, 
                             title=request.POST.get('title'),
                             text=request.POST.get('text'),
                             soundtrack=request.FILES.get('soundtrack'))
            instance.save()
            return redirect(reverse('track_list'))
        else:
            messages.error(request, u'Что-то неправильно.')
    else:
        track_form = TrackForm()
    return render(request, 'soundtracks/track_add.html', {
        'form': track_form
    })


class TrackCreate(CreateView): 
    model = Track
    form_class = TrackForm
    template_name = "soundtracks/track_add.html"
    success_url = reverse_lazy("track_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        peaks, duration = make_peaks(self.request.FILES.get('soundtrack'))
        if peaks:
            form.instance.peaks = peaks
            form.instance.duration = duration
        return super(TrackCreate, self).form_valid(form)


class TrackDelete(TemplateView):
    model = Track
    form_class = TrackDeleteForm
    template_name = "soundtracks/track_delete.html"
    comment = None

    def post(self, request, *args, **kwargs):
        self.track = Track.objects.get(pk = self.kwargs["pk"])
        if self.track.author == request.user or request.user.is_superuser:
            self.track.delete()
            redirect_url = reverse("track_list")
            return redirect(redirect_url)
        else:
            return redirect(reverse("login"))


class TrackUpdate(TemplateView):
    track = None
    template_name = "soundtracks/track_edit.html"
    form = None
    fields = "__all__"

    def get(self, request, *args, **kwargs):
        self.track = Track.objects.get(pk = self.kwargs["pk"])
        if self.track.author == request.user or request.user.is_superuser:
            self.form = TrackForm(instance = self.track)
            return super(TrackUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("login"))

    def get_context_data(self, **kwargs):
        context = super(TrackUpdate, self).get_context_data(**kwargs)
        context["track"] = self.track
        context["form"] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.track = Track.objects.get(pk = self.kwargs["pk"])
        if self.track.author == request.user or request.user.is_superuser:
            self.form = TrackForm(request.POST, request.FILES, instance = self.track)
            if self.form.is_valid():
                peaks, duration = make_peaks(request.FILES.get('soundtrack'))
                if peaks:
                    self.form.instance.peaks = peaks
                    self.form.instance.duration = duration
                self.form.save()
                redirect_url = reverse("track_detail", kwargs={"pk" : self.track.pk})
                return redirect(redirect_url)
            else:
                return super(TrackUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("login"))


class CommentCreate(TemplateView):
    template_name = "soundtrack/comment_add.html"
    track_pk = None
    form = None

    def post(self, request, *args, **kwargs):
        self.track_pk = self.kwargs["pk"]
        #print(self.request.user.username)
        if self.request.user:
            comment_text = self.request.POST.get('comment')
            track = Track.objects.get(pk = self.track_pk)
            comment = TrackComment(parent_track=track, 
                   author=self.request.user, content=comment_text)
            comment.save()
            response_data = {}
            response_data['result'] = 'Comment created!'
            response_data['content'] = comment.content
            response_data['datetime'] = comment.datetime
            response_data['author'] = comment.author.username
            return JsonResponse(response_data)
        else:
            redirect_url = reverse("track_detail", kwargs={"pk" : self.track_pk})
            return redirect(redirect_url)


class CommentDelete(TemplateView):
    model = TrackComment
    form_class = CommentDeleteForm
    template_name = "soundtracks/comment_delete.html"
    comment = None

    def post(self, request, *args, **kwargs):
        self.comment = TrackComment.objects.get(pk = self.kwargs["pk"])
        #print(self.comment.author)
        if self.comment.author == request.user or request.user.is_superuser:
            self.comment.delete()
            redirect_url = reverse("track_detail", kwargs={"pk" : self.comment.parent_track.pk})
            return redirect(redirect_url)
        else:
            return redirect(reverse("login"))