# coding: utf-8
import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Post, Comment


class PostModelTests(TestCase):

  def test_last_posts_have_right_time(self):
    user = User.objects.create(username='test_user')
    post1 = Post.objects.create(author=user, title='test_title1', content='test_content1',
           datetime=timezone.now())
    post2 = Post.objects.create(author=user, title='test_title2', content='test_content2',
           datetime=timezone.now() - datetime.timedelta(days=1))
    posts = Post.objects.all()[:2]
    self.assertIs(posts[0].datetime > posts[1].datetime, True)


class PostListViewTest(TestCase):

  def test_no_posts(self):
    response = self.client.get(reverse('list'))
    self.assertEqual(response.status_code, 200)
    # checking class 'no-posts' in tag, instead of inner text because of trans tag
    self.assertContains(response, 'no-posts') 
    self.assertQuerysetEqual(response.context['object_list'], [])

  def test_past_post(self):
    user = User.objects.create(username='test_user')
    post = Post.objects.create(author=user, title='test_title', content='test_content')
    response = self.client.get(reverse('list'))
    self.assertQuerysetEqual(
      response.context['object_list'],
      ['<Post: test_title>']
    )

class PostDetailViewTest(TestCase):

  def test_get_post(self):
    user = User.objects.create(username='test_user')
    post = Post.objects.create(author=user, title='test_title', content='test_content')
    response = self.client.get(reverse('post_detail', args=(post.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Комментарии:')
    self.assertQuerysetEqual(response.context['comments'], [])