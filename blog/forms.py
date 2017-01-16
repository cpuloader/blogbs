#coding: utf-8
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import Post, Comment #UserExtraFields

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        #fields = ('author', 'title', 'content',)
        #widgets = {'author': forms.HiddenInput(),}

class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('parent_post', 'author', 'content',)
        widgets = {'parent_post': forms.HiddenInput(), 'author': forms.HiddenInput(),}

class CommentRemoveForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('parent_post', 'author')

