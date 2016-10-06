#coding: utf-8
import hashlib
import datetime
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import TempUrl
from .forms import TempUrlForm


class EnterTextView(CreateView): 
    model = TempUrl
    form_class = TempUrlForm
    template_name = "tempurls/enter.html"
    success_url = reverse_lazy("link_ready")
    form = None
    expires = ""

    def form_valid(self, form):
        form.instance.text = form.cleaned_data['text'].encode('utf-8')
        user = self.request.user
        form.instance.expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(seconds=150), "%Y-%m-%d %H:%M:%S")
        m = hashlib.md5(user.username.encode('utf-8') + form.instance.text).hexdigest()[:12]
        print("Expires:", str(form.instance.expires).encode('utf-8'))
        form.instance.url_hash = m
        data = {"username": user.username, "url_hash": form.instance.url_hash, 
                       "email": user.email, "expires": form.instance.expires}
        form.SendEmail(data)
        return super(EnterTextView, self).form_valid(form)


class ShowLinkView(TemplateView):
    model = TempUrl
    fields = "__all__"
    template_name = "tempurls/link.html"


class ShowTextView(TemplateView):
    model = TempUrl
    fields = "__all__"
    template_name = "tempurls/show.html"
    _secret = ""
    error = ""

    def get(self, request, *args, **kwargs):
        url_hash = kwargs['key']
        temp_url = get_object_or_404(TempUrl, url_hash = kwargs['key'])
        if timezone.now() > temp_url.expires:
            self.error = "Ссылка просрочена!"
            return super(ShowTextView, self).get(request, *args, **kwargs)
        if self.request.user.is_active:
            m = hashlib.md5(self.request.user.username.encode('utf-8') +
                       temp_url.text.encode('utf-8')).hexdigest()[:12]
            if m != url_hash:
                self.error = "Хэш не совпадает! Наверно не тот юзер."
                return super(ShowTextView, self).get(request, *args, **kwargs)
            else:
                self._secret = temp_url.text
        print(self._secret)
        return super(ShowTextView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShowTextView, self).get_context_data(**kwargs)
        context["secret"] = self._secret
        context["error"] = self.error
        return context
