# coding: utf-8
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
#import json
#from django.http import HttpResponse

from .models import Post, Comment
from .forms import PostForm, PostDeleteForm, CommentForm, CommentRemoveForm

class PostList(ListView): 
    model = Post               
    fields = "__all__"
    success_url = reverse_lazy("list")

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        initial = None
        if self.request.session.pop('tupo', None):
            title = self.request.session.pop('post_form_title','')
            content = self.request.session.pop('post_form_content','')
            initial = {'title': title, 'content': content }
        context["post_form"] = PostForm(initial)
        return context


class PostCreate(CreateView): 
    model = Post
    form_class = PostForm
    template_name = "blog/post_add.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session['tupo'] = 'yes'
        self.request.session['post_form_title'] = form.instance.title
        self.request.session['post_form_content'] = form.instance.content
        return redirect(reverse('list'))


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    success_url = reverse_lazy("list")

    def get(self, request, *args, **kwargs):
        self.post = Post.objects.get(pk = self.kwargs["pk"])
        return super(PostDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        user = self.request.user
        initial_data = {'parent_post': self.kwargs["pk"], 'author': user }
        if self.request.session.pop('comment_tupo', None):
            content = self.request.session.pop('comment_form_content','')
            initial_data.update(content = content)
        context["comment_form"] = CommentForm(initial = initial_data)
        context["comment_remove_form"] = CommentRemoveForm(initial = {'parent_post': self.kwargs["pk"]})
        context["comments"] = self.post.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        #self.post = Post.objects.get(pk = self.kwargs["pk"])
        redirect_url = reverse("list")
        return redirect(redirect_url)    


class PostUpdate(TemplateView):
    post = None
    template_name = "blog/post_edit.html"
    form = None
    fields = "__all__"

    def get(self, request, *args, **kwargs):
        self.post = Post.objects.get(pk = self.kwargs["pk"])
        if self.post.author == request.user or request.user.is_superuser:
            self.form = PostForm(instance = self.post)
            return super(PostUpdate, self).get(request, *args, **kwargs)
        else:
            #messages.add_message(request, messages.ERROR, "Поле не может быть пустым.")
            #redirect_url = reverse("post_detail", kwargs={"pk" : self.post_pk})
            return redirect(reverse("login"))

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)
        context["post"] = self.post
        context["form"] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.post = Post.objects.get(pk = self.kwargs["pk"])
        if self.post.author == request.user or request.user.is_superuser:
            self.form = PostForm(request.POST, instance = self.post)
            if self.form.is_valid():
                self.form.save()
                redirect_url = reverse("post_detail", kwargs={"pk" : self.post.pk})
                return redirect(redirect_url)
            else:
                return super(PostUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("login"))

class PostDelete(TemplateView):
    post = None
    template_name = "blog/post_delete.html"
    form_class = PostDeleteForm

    def post(self, request, *args, **kwargs):
        self.post = Post.objects.get(pk = self.kwargs["pk"])
        if self.post.author == request.user or request.user.is_superuser:
            self.post.delete()
            redirect_url = reverse("list")
            return redirect(redirect_url)
        else:
            return redirect(reverse("login"))


class CommentCreate(TemplateView):
    template_name = "blog/comment_add.html"
    post_pk = None
    form = None

    def post(self, request, *args, **kwargs):
        self.post_pk = self.kwargs["pk"]
        self.form = CommentForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            redirect_url = reverse("post_detail", kwargs={"pk" : self.post_pk})
            return redirect(redirect_url)
        else:
            self.request.session['comment_tupo'] = 'yes'
            self.request.session['comment_form_content'] = self.form.instance.content
            messages.add_message(request, messages.ERROR, "Поле не может быть пустым.")
            redirect_url = reverse("post_detail", kwargs={"pk" : self.post_pk})
            return redirect(redirect_url)


class CommentRemove(TemplateView):
    model = Comment
    form_class = CommentRemoveForm
    template_name = "blog/comment_remove.html"
    comment = None

    def post(self, request, *args, **kwargs):
        self.comment = Comment.objects.get(pk = self.kwargs["pk"])
        if self.comment.author == request.user or request.user.is_superuser:
            self.comment.delete()
            redirect_url = reverse("post_detail", kwargs={"pk" : self.comment.parent_post.pk})
            return redirect(redirect_url)
        else:
            return redirect(reverse("login"))