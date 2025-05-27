from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from jedi.inference.flow_analysis import Status

from .models import Post


def index(request):
    posts = get_list_or_404(Post,status=Post.Status.PUBLISHED)

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
