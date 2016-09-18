from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
#import json
#from django.http import HttpResponse

from .models import Post
from .forms import PostForm

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
"""
def myscript(request):
  output = {}
  output["images"] = []
  return HttpResponse(json.dumps(output), content_type = "application/json")
"""