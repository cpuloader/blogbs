from django import forms
from .models import TextToSay
#from django.utils.translation import ugettext_lazy as _

class SpeakForm(forms.ModelForm):

    class Meta:
    
        model = TextToSay
        fields = ('text_to_say',)
        widgets = {'text': forms.Textarea}

