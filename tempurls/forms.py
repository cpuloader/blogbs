#coding: utf-8
import pip._vendor.requests as requests
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail #, EmailMultiAlternatives

from .models import TempUrl
import blogbootstrap.settings as settings

sitelink = settings.ALLOWED_HOSTS[0]
#sender = settings.DEFAULT_FROM_EMAIL

class TempUrlForm(forms.ModelForm):
    #text = forms.CharField()
    #text.label = u'Введи секретный текст'.encode('utf-8')

    class Meta:
        model = TempUrl
        fields = ('text', )
        widgets = {'text': forms.HiddenInput(), }

    def SendEmail(self, datas):
        start = "<!DOCTYPE html> \n <html lang='ru'> \n" + "<body style='background-color:#7FFFD4;'> \n <a href='"
        end = '\n</body>\n</html>'
        link = "http://" + sitelink + "/tempurls/temp/" + datas['url_hash'] 
        html_content = start + link + "'>Link</a>" + '\n<p>User: ' + datas["username"] + '</p>\n<p>Link expires: ' + datas["expires"] + "</p>" + end
        text_content = link + '\nUser: ' + datas["username"] + '\nLink expires: ' + datas["expires"]
        #msg = EmailMultiAlternatives("Secret link", text_content, sender, [datas['email']])
        #msg.attach_alternative(html_content, "text/html")
        #msg.send(fail_silently=False)

        #send_mail("Secret link", text_content, sender, [datas['email']], fail_silently=True)

        #return requests.post(
        #"https://api.mailgun.net/v3/sandbox3debeca907c54d94bd4edc1548d5f2d3.mailgun.org/messages",
        #auth=("api", "key-8668f638ba7f7229bbc457863d303ca2"),
        #data={"from": "Mailgun Sandbox <postmaster@sandbox3debeca907c54d94bd4edc1548d5f2d3.mailgun.org>",
        #      "to": datas['email'],
        #      "subject": "Secret link",
        #      "text": text_content })
    
