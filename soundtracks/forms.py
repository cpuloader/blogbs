#coding: utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Track, TrackComment

def file_size(value):
    limit = 150 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(u'Размер файла превышает 150Мб.')

class TrackForm(forms.ModelForm):
    soundtrack = forms.FileField(required=True, label=u'Аудиофайл', validators=[file_size])
    class Meta:
        model = Track
        fields = ('title', 'text', 'soundtrack',) #'__all__'

class TrackDeleteForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = TrackComment
        fields = ('content',)
        widgets = {'content': forms.TextInput,} #'author': forms.HiddenInput(),

class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = TrackComment
        fields = '__all__' #('parent_track',)