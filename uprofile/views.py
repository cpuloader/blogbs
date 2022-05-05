#coding: utf-8
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import NewUserForm, UserForm, ProfileForm
from .models import UserExtraFields


@transaction.atomic
def user_create(request): 
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile.baseuser = new_user
            new_profile.save()
            return redirect(reverse('login'))
        else:
            messages.error(request, u'Что-то неправильно.')
    else:
        user_form = NewUserForm()
        profile_form = ProfileForm()
    return render(request, 'uprofile/user_add.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_profile(request, pk): 
    user = get_object_or_404(User, pk=pk)
    return render(request, 'uprofile/user_profile.html', {
        'userdata': user
    })

@login_required
@transaction.atomic
def user_update(request, pk): 
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and user == request.user:
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.userextrafields)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile.baseuser = new_user
            new_profile.save()
            return redirect('user_profile', pk=user.pk)
        else:
            messages.error(request, u'Произошла ошибка.')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.userextrafields)
    return render(request, 'uprofile/user_profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

