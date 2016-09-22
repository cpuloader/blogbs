from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
#import json
#from django.http import HttpResponse

from .models import Post
from .forms import PostForm, MyRegistrationForm

class PostsListView(ListView): 
    model = Post               
    fields = "__all__"
    success_url = reverse_lazy("list")

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context["post_form"] = PostForm()
        return context

class PostDetailView(DetailView): 
    model = Post
    fields = "__all__"

class PostCreateView(CreateView): 
    model = Post
    form_class = PostForm
    template_name = "blog/post_add.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class UserCreateView(TemplateView): 
    template_name = "blog/user_add.html"
    form = None

    def get(self, request, *args, **kwargs):
        self.form = MyRegistrationForm()
        return super(UserCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context["form"] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.form = MyRegistrationForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse("list"))
        self.form = MyRegistrationForm(request.POST)
        return super(UserCreateView, self).get(request, *args, **kwargs)
