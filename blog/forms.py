#from __future__ import unicode_literals
#from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm

from .models import Post, UserExtraFields

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class MyRegistrationForm(UserCreationForm):
    text = forms.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.text = self.cleaned_data['text']
        if commit:
            user.save()
            permission = Permission.objects.get(name='Can add post')
            user.user_permissions.add(permission)
            UserExtraFields.objects.create(user=user, text=unicode(user.text, 'utf-8'))
        return user

