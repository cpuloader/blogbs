#coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from .models import TempUrl
import blogbootstrap.settings as settings

sitelink = settings.ALLOWED_HOSTS[0]
sender = settings.DEFAULT_FROM_EMAIL

class TempUrlForm(forms.ModelForm):
    #text = forms.CharField()
    #text.label = u'Введи секретный текст'.encode('utf-8')

    class Meta:
        model = TempUrl
        fields = ('text',)
        widgets = {'text': forms.HiddenInput(),}

    def SendEmail(self, data):
        link = "http://" + sitelink + "/tempurls/temp/" + data['url_hash']
        message = link + '   User: ' + data["username"] + '   Link expires: ' + data["expires"]
        #print unicode(message).encode('utf8')
        send_mail("Secret link", message, sender, 
                            [data['email']], fail_silently=False)
