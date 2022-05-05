from django import forms
from .models import TextToSay
#from django.utils.translation import gettext_lazy as _

class SpeakForm(forms.ModelForm):

    class Meta:
    
        model = TextToSay
        fields = ('text_to_say', 'auto_next',)
        widgets = {'text': forms.Textarea}

