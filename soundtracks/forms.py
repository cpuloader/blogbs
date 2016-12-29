#coding: utf-8
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import Track, TrackComment

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = '__all__'

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