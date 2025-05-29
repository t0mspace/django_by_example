from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import Post

def index(request):
  posts = get_list_or_404(Post, status=Post.Status.PUBLISHED)
  paginator = Paginator(posts, 10)
  page_number = request.GET.get('page', 1)
  try:
    posts = paginator.page(page_number)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  return render(request, 'blog/post/list.html', {
    'posts': posts,
  })

def detail(request, year, month, day, post):
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day
                           )
  return render(request, 'blog/post/detail.html', {
    'post': post,
  })
