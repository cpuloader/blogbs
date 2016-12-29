#coding: utf-8
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import Post, Comment, UserExtraFields

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
        fields = ('parent_post',)

class MyRegistrationForm(UserCreationForm):
    text = forms.CharField(required = False, widget=forms.Textarea)
    text.label = _(u'Немного о себе') #.encode('utf-8')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.text = self.cleaned_data['text']
        if commit:
            user.save()
            baseuser = User.objects.get(username='baseuser')
            base_perms = baseuser.user_permissions.all()
            for p in base_perms:
                print(p.codename)
                perm = Permission.objects.get(name=p.name)
                user.user_permissions.add(perm)
            UserExtraFields.objects.create(user=user, text=user.text.encode('utf-8'))
        return user