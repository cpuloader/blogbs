#coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm

import blogbootstrap.settings as settings
from .models import UserExtraFields

def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(u'Размер файла превышает 2Мб.')

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        if commit:
            #print('creating user')
            user.save()
            baseuser = User.objects.get(username='baseuser')
            base_perms = baseuser.user_permissions.all()
            for p in base_perms:
                perm = Permission.objects.get(name=p.name)
                user.user_permissions.add(perm)
                #print('adding perms')
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False, validators=[file_size], label=u'Фото')

    class Meta:
        model = UserExtraFields
        fields = ('text', 'picture')
