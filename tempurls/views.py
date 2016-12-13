#coding: utf-8
import hashlib, os, random
import datetime
from shutil import copyfile

from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from wsgiref.util import FileWrapper as myFileWrapper
from django.utils.translation import ugettext as _

import blogbootstrap.settings as settings

from .models import TempUrl
from .forms import TempUrlForm



class EnterTextView(CreateView): 
    model = TempUrl
    form_class = TempUrlForm
    template_name = "tempurls/enter.html"
    success_url = reverse_lazy("link_ready")
    form = None
    expires = ""
    
    def get(self, request, *args, **kwargs):
        alltempurls = TempUrl.objects.all()
        if alltempurls:
            basedir = os.path.split(settings.BASEFILE)[0]
            for temp_url in alltempurls:
                if timezone.now() > temp_url.expires:
                    temp_url.delete()
                    yourfile = os.path.join(basedir, temp_url.text + '.zip')
                    try:
                        os.remove(yourfile)
                    except EnvironmentError:
                        pass
        return super(EnterTextView, self).get(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        #form.instance.text = form.cleaned_data['text'].encode('utf-8')
        form.instance.text = hashlib.sha1(str(random.random())).hexdigest()[:5]
        user = self.request.user
        form.instance.expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(seconds=600), "%Y-%m-%d %H:%M:%S")
        m = hashlib.md5(user.username.encode('utf-8') + form.instance.text).hexdigest()[:12]
        #print("Expires:", str(form.instance.expires).encode('utf-8'))
        #print(self.request.user)
        form.instance.url_hash = m
        #print(form.instance.url_hash)
        data = {"username": user.username, "url_hash": form.instance.url_hash,
                       "email": user.email, "expires": form.instance.expires}
        form.SendEmail(data)
        return super(EnterTextView, self).form_valid(form)


class ShowLinkView(TemplateView):
    model = TempUrl
    fields = "__all__"
    template_name = "tempurls/link.html"


def your_file(request, key):
    url_hash = key
    temp_url = get_object_or_404(TempUrl, url_hash = key)
    basedir = os.path.split(settings.BASEFILE)[0]
    yourfile = os.path.join(basedir, temp_url.text + '.zip')
    copyfile(settings.BASEFILE, yourfile)
    if timezone.now() > temp_url.expires:
        error = _(u'Ссылка просрочена!')
        try:
            os.remove(yourfile)
        except EnvironmentError:
            pass
        return render(request, 'tempurls/show.html', {'error' : error})
    if request.user.is_active:
        m = hashlib.md5(request.user.username.encode('utf-8') +
                     temp_url.text.encode('utf-8')).hexdigest()[:12]
        if m != url_hash:
            error = _(u'Хэш не совпадает! Наверно не тот юзер.')
            return render(request, 'tempurls/show.html', {'error' : error})
    else:
        error = _(u'Нужно войти под своим аккаунтом, чтобы скачать файл!')
        return render(request, 'tempurls/show.html', {'error' : error})
    wrapper = myFileWrapper(open(yourfile, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(yourfile)
    response['Content-Length'] = os.path.getsize(yourfile)
    return response
