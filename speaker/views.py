from gtts import gTTS
import os, urllib
import datetime
import hashlib, random
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.core.files.base import File as DjangoFile

from .models import TextToSay
from .forms import SpeakForm
import blogbootstrap.settings as settings


class JavaScriptView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = "application/javascript"
        return super(JavaScriptView, self).render_to_response(
            context, **response_kwargs)

tplayer_script = JavaScriptView.as_view(template_name="speaker/tplayer.js")

def enter_new_text(request):
    all_texts = TextToSay.objects.all()
    if all_texts:
        #basedir = os.path.split(settings.BASEFILE)[0]
        for text in all_texts:
            if timezone.now() > text.expires:
                text.delete()
                #yourfile = os.path.join(basedir, temp_url.text + '.zip')
                #try:
                #    #os.remove(yourfile)
                #    os.remove(text.file_to_play)
                #except EnvironmentError:
                #    pass
    if request.method == "POST":
        form = SpeakForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.save(commit=False)
            tts = gTTS(text=text.text_to_say, lang='ru')
            dirpath = os.path.join(settings.MEDIA_ROOT, 'speaker_mp3s')
            filename = hashlib.sha1(str(random.random())).hexdigest()[:5] + '.mp3'
            fullpath = os.path.join(dirpath, filename)
            tts.save(fullpath)
            f = open(fullpath, 'rb')
            django_file = DjangoFile(f)
            #text.file_to_play = DjangoFile(f)
            text.file_to_play.save(filename, django_file, save=True)
            #text.file_to_play = filename
            text.expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(seconds=100), "%Y-%m-%d %H:%M:%S")
            text.save()
            #print(text.expires)
            f.close()
            os.remove(fullpath)
            return redirect('play_text', pk=text.pk)
    else:
        form = SpeakForm()
    return render(request, 'speaker/enter_text.html', {'form' : form})

def play_new_text(request, pk):
    text = get_object_or_404(TextToSay, pk=pk)
    #text.file_url = urllib.pathname2url(text.file_to_play)
    return render(request, 'speaker/play_text.html', {'text' : text})
